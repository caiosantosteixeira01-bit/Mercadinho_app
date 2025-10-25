from models import User, Product

def seed():
    # Usuários
    users = [
        ("Admin", "admin@mercadinho.com", "999999999", "admin123", 1),
        ("Moderador", "mod@mercadinho.com", "888888888", "mod123", 2),
        ("Limitado", "limitado@mercadinho.com", "777777777", "limit123", 3)
    ]
    for u in users:
        User.create(*u)

    # Produtos
    products = [
        ("Arroz", "Alimentos", 50, 10.0, 15.0),
        ("Feijão", "Alimentos", 30, 8.0, 12.0),
        ("Leite", "Bebidas", 20, 4.0, 6.0)
    ]
    for p in products:
        Product.create(*p)

if __name__ == "__main__":
    seed()
    print("Seed inicial criado!")
