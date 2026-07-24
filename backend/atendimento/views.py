from django.utils import timezone
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from .models import Atendimento
from .serializers import AtendimentoSerializer

from accounts.permissions import IsAdvogadoOuSecretaria

from .models import SolicitacaoAtendimento
from .serializers import SolicitacaoCreateSerializer, SolicitacaoSerializer


class SolicitacaoCreateView(CreateAPIView):
    """
    RF01 — endpoint público do site. Qualquer visitante pode enviar uma
    solicitação de atendimento, sem estar logado.
    """

    serializer_class = SolicitacaoCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Hoje o sistema opera com um único escritório (Advocacia Neves).
        # Quando houver mais de um tenant, isso precisará vir de outro
        # lugar (ex: subdomínio ou slug na URL pública).
        from core.models import Escritorio

        escritorio = Escritorio.objects.filter(ativo=True).first()
        serializer.save(escritorio=escritorio)


class SolicitacaoListView(ListAPIView):
    """RF07 — secretaria/admin visualizam todas as solicitações."""

    queryset = SolicitacaoAtendimento.objects.all()
    serializer_class = SolicitacaoSerializer
    permission_classes = [IsAdvogadoOuSecretaria]


class SolicitacaoAprovarView(APIView):
    """
    RF08 — aprova uma solicitação pendente.

    - Se `urgente=True`: já cria o Usuario (role=cliente) e o Cliente
      vinculado nesse momento, sem etapa manual — para casos que não
      podem esperar (ex: audiência marcada para o dia seguinte).
    - Se `urgente=False`: apenas muda o status para "aprovada". A
      secretaria cadastra o Cliente manualmente depois, com calma.
    """

    permission_classes = [IsAdvogadoOuSecretaria]

    def post(self, request, pk):
        solicitacao = SolicitacaoAtendimento.objects.get(pk=pk)
        if solicitacao.status != SolicitacaoAtendimento.Status.PENDENTE:
            return Response(
                {"detail": "Esta solicitação já foi analisada."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        solicitacao.status = SolicitacaoAtendimento.Status.APROVADA
        solicitacao.analisado_em = timezone.now()
        solicitacao.save()

        cliente_criado = None
        if solicitacao.urgente:
            cliente_criado = self._criar_cliente_automaticamente(solicitacao)

        data = SolicitacaoSerializer(solicitacao).data
        if cliente_criado:
            data["cliente_criado_id"] = str(cliente_criado.id)
        return Response(data)

    def _criar_cliente_automaticamente(self, solicitacao):
        import secrets

        from accounts.models import PasswordResetToken, Role, Usuario
        from clientes.models import Cliente

        usuario = Usuario.objects.create_user(
            email=solicitacao.email,
            password=None,  # sem senha até o cliente definir a própria
            role=Role.CLIENTE,
            escritorio=solicitacao.escritorio,
        )
        usuario.set_unusable_password()
        usuario.first_name = solicitacao.nome
        usuario.save()

        token = secrets.token_urlsafe(48)
        PasswordResetToken.objects.create(usuario=usuario, token=token)
        print(f"[cliente-urgente] link para definir senha de {usuario.email}: /reset-password?token={token}")

        return Cliente.objects.create(
            escritorio=solicitacao.escritorio,
            usuario=usuario,
            solicitacao_origem=solicitacao,
            nome=solicitacao.nome,
            email=solicitacao.email,
            telefone=solicitacao.telefone,
        )

class SolicitacaoRecusarView(APIView):
    """RF08 — recusa uma solicitação pendente, com motivo opcional."""

    permission_classes = [IsAdvogadoOuSecretaria]

    def post(self, request, pk):
        solicitacao = SolicitacaoAtendimento.objects.get(pk=pk)
        if solicitacao.status != SolicitacaoAtendimento.Status.PENDENTE:
            return Response(
                {"detail": "Esta solicitação já foi analisada."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        solicitacao.status = SolicitacaoAtendimento.Status.RECUSADA
        solicitacao.motivo_recusa = request.data.get("motivo", "")
        solicitacao.analisado_em = timezone.now()
        solicitacao.save()
        return Response(SolicitacaoSerializer(solicitacao).data)


class AtendimentoViewSet(viewsets.ModelViewSet):
    serializer_class = AtendimentoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Atendimento.objects.filter(escritorio=self.request.user.escritorio)

    def perform_create(self, serializer):
        serializer.save(escritorio=self.request.user.escritorio)