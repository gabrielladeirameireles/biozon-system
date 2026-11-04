import secrets
from urllib.parse import quote

class InviteService:

    @staticmethod
    def generate_token() -> str:
        return secrets.token_urlsafe(32)

    @staticmethod
    def build_whatsapp_invite_link(phone: str, collaborator_name: str, invite_token: str, sender_name: str = "Getúlio") -> str:
        clean_phone = "".join(filter(str.isdigit, phone))
        if not clean_phone.startswith("55"):
            clean_phone = f"55{clean_phone}"

        invite_url = f"https://biozon.com.br/admin/register?token={invite_token}"
        message = (
            f"Olá {collaborator_name}, você foi convidado por {sender_name} para integrar a equipe do painel administrativo da BIOZON.\n\n"
            f"Conclua o seu cadastro acessando o link seguro: {invite_url}"
        )
        
        encoded_message = quote(message)
        return f"https://wa.me/{clean_phone}?text={encoded_message}"

    @staticmethod
    def build_email_invite_payload(email: str, collaborator_name: str, invite_token: str, sender_name: str = "Getúlio") -> dict:
        invite_url = f"https://biozon.com.br/admin/register?token={invite_token}"
        return {
            "to": email,
            "subject": "Convite para Painel Administrativo BIOZON",
            "body": (
                f"Olá {collaborator_name},\n\n"
                f"{sender_name} convidou você para o painel de controle da BIOZON.\n"
                f"Para definir sua senha e ativar sua conta, acesse:\n{invite_url}\n\n"
                "Atenciosamente,\nEquipe BIOZON Purificadores"
            )
        }


    