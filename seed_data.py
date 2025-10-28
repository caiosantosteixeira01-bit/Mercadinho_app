from models import User, Product, get_all_users, get_all_products

def seed():
    # --- Usuários existentes ---
    users = get_all_users()
    existing_emails = [u[2] for u in users]  # pega todos os emails existentes

    # --- Usuários principais ---
    if "admin@mercadinho.com" not in existing_emails:
        User.create("Admin","admin@mercadinho.com","1111","admin123","Admin")
    if "mod@mercadinho.com" not in existing_emails:
        User.create("Moderador","mod@mercadinho.com","2222","mod123","Moderador")
    if "limitado@mercadinho.com" not in existing_emails:
        User.create("Limitado","limitado@mercadinho.com","3333","limit123","Limitado")

    # --- NOVO USUÁRIO DE TESTE (Admin) ---
    if "teste@admin.com" not in existing_emails:
        User.create("Teste Admin","teste@admin.com","4444","teste123","Admin")
        print("Usuário de teste criado: teste@admin.com / senha: teste123")

    # --- Produtos ---
    produtos = [p[1] for p in get_all_products()]
    if "Arroz" not in produtos:
        Product.create("Arroz",50,20.0)
    if "Feijão" not in produtos:
        Product.create("Feijão",30,15.0)
    if "Macarrão" not in produtos:
        Product.create("Macarrão",40,8.0)

# --- Chamando o seed ao executar o arquivo ---
if __name__ == "__main__":
    seed()
