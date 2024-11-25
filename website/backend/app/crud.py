from models.users import Users
from sqlalchemy.orm import sessionmaker, Session
from models.product import ProductModel  # Supposons que le modèle SQLAlchemy soit défini
from sqlalchemy.orm import Session
from typing import List

from utils.llm_file import get_response


products_test = [
    {
        "id": 1,
        "main_category": "All Beauty",
        "title": "Lurrose 100Pcs Full Cover Fake Toenails",
        "average_rating": 3.7,
        "rating_number": 35,
        "features": [
            "The false toenails are durable with perfect length.",
            "ABS is kind of green environmental material.",
            "Fit well to your natural toenails.",
            "Wonderful as gift for girlfriend, family and friends.",
            "The easiest and most efficient way to do your toenail tips for manicures or nail art designs."
        ],
        "description": [
            "Description",
            "The false toenails are durable with perfect length. You have the option to wear them long or clip them short, easy to trim and file them to any length and shape you like.",
            "Feature",
            "- Color: As Shown.- Material: ABS.- Size: 14.3 x 7.2 x 1cm.",
            "Package Including",
            "100 x Pieces fake toenails"
        ],
        "price": 6.99,
        "images": [
            {
                "hi_res": "https://m.media-amazon.com/images/I/41a1Sj7Q20L._SL1005_.jpg",
                "thumb": "https://m.media-amazon.com/images/I/31dlCd7tHSL._SS40_.jpg",
                "large": "https://m.media-amazon.com/images/I/31dlCd7tHSL.jpg",
                "variant": "MAIN"
            }
        ],
        "videos": [],
        "store": "Lurrose",
        "categories": [],
        "details": {
            "Color": "As Shown",
            "Size": "Large",
            "Material": "Acrylonitrile Butadiene Styrene (ABS)",
            "Brand": "Lurrose",
            "Style": "French",
            "Product Dimensions": "5.63 x 2.83 x 0.39 inches; 1.9 Ounces",
            "UPC": "799768026253",
            "Manufacturer": "Lurrose"
        },
        "parent_asin": "B07G9GWFSM",
        "bought_together": None
    },
    {
        "id": 2,
        "main_category": "Electronics",
        "title": "Anker Soundcore 2 Bluetooth Speaker",
        "average_rating": 4.5,
        "rating_number": 1500,
        "features": [
            "Superior sound quality with enhanced bass.",
            "IPX7 waterproof, perfect for outdoor use.",
            "24-hour playtime on a single charge.",
            "Bluetooth 5.0 for a stable connection.",
            "Compact and portable design, easy to carry."
        ],
        "description": [
            "Description",
            "The Anker Soundcore 2 Bluetooth speaker offers impressive sound quality and powerful bass in a compact and portable design. With a 24-hour playtime and IPX7 waterproof rating, it’s perfect for both indoor and outdoor use.",
            "Feature",
            "- Color: Black.- Material: ABS.- Size: 6.5 x 2.1 x 2.2 inches.",
            "Package Including",
            "1 x Anker Soundcore 2 Bluetooth Speaker, 1 x Micro USB Charging Cable, 1 x User Manual"
        ],
        "price": 39.99,
        "images": [
            {
                "hi_res": "https://m.media-amazon.com/images/I/81-wG7n2l3L._SL1500_.jpg",
                "thumb": "https://m.media-amazon.com/images/I/61VvMhbQEdL._SS40_.jpg",
                "large": "https://m.media-amazon.com/images/I/61VvMhbQEdL.jpg",
                "variant": "MAIN"
            }
        ],
        "videos": [],
        "store": "Anker",
        "categories": [],
        "details": {
            "Color": "Black",
            "Size": "Compact",
            "Material": "Plastic",
            "Brand": "Anker",
            "Style": "Bluetooth Speaker",
            "Product Dimensions": "6.5 x 2.1 x 2.2 inches; 12 ounces",
            "UPC": "848061066479",
            "Manufacturer": "Anker"
        },
        "parent_asin": "B01MTB55WF",
        "bought_together": None
    },
    {
        "id": 3,
        "main_category": "Home & Kitchen",
        "title": "Instant Pot Duo 7-in-1 Electric Pressure Cooker",
        "average_rating": 4.7,
        "rating_number": 5500,
        "features": [
            "Pressure cooker, slow cooker, rice cooker, steamer, sauté, yogurt maker, and warmer.",
            "Large 6-quart capacity.",
            "Easy-to-use, one-touch control panel.",
            "Stainless steel inner pot for easy cleanup.",
            "Over 10 safety features."
        ],
        "description": [
            "Description",
            "The Instant Pot Duo is a 7-in-1 multi-cooker that combines the functions of a pressure cooker, slow cooker, rice cooker, steamer, and more. It features a large 6-quart capacity and is designed for quick, healthy meals.",
            "Feature",
            "- Color: Stainless Steel.- Material: Stainless Steel.- Size: 13 x 12 x 12 inches.",
            "Package Including",
            "1 x Instant Pot Duo 7-in-1 Electric Pressure Cooker, 1 x Stainless Steel Inner Pot, 1 x User Manual"
        ],
        "price": 89.99,
        "images": [
            {
                "hi_res": "https://m.media-amazon.com/images/I/71-u8uHwrWL._SL1500_.jpg",
                "thumb": "https://m.media-amazon.com/images/I/71e1Vkk5HoL._SS40_.jpg",
                "large": "https://m.media-amazon.com/images/I/71e1Vkk5HoL.jpg",
                "variant": "MAIN"
            }
        ],
        "videos": [],
        "store": "Instant Pot",
        "categories": [],
        "details": {
            "Color": "Stainless Steel",
            "Size": "6-Quart",
            "Material": "Stainless Steel",
            "Brand": "Instant Pot",
            "Style": "7-in-1 Multi-Cooker",
            "Product Dimensions": "13 x 12 x 12 inches; 13 pounds",
            "UPC": "853084004643",
            "Manufacturer": "Instant Pot"
        },
        "parent_asin": "B08PQ2D6Z1",
        "bought_together": None
    },
    {
        "id": 4,
        "main_category": "Toys & Games",
        "title": "LEGO Star Wars X-Wing Starfighter",
        "average_rating": 4.9,
        "rating_number": 3000,
        "features": [
            "Detailed buildable X-Wing Starfighter model.",
            "Includes minifigures of Luke Skywalker, Princess Leia, and R2-D2.",
            "Wings that open and close with a trigger mechanism.",
            "Perfect for Star Wars fans and collectors.",
            "Over 700 pieces for a challenging build."
        ],
        "description": [
            "Description",
            "Build your own X-Wing Starfighter with this detailed LEGO set. The model features wings that open and close, along with iconic Star Wars minifigures like Luke Skywalker and Princess Leia.",
            "Feature",
            "- Color: Multi.- Material: Plastic.- Size: 12 x 10 x 6 inches.",
            "Package Including",
            "1 x LEGO Star Wars X-Wing Starfighter set"
        ],
        "price": 59.99,
        "images": [
            {
                "hi_res": "https://m.media-amazon.com/images/I/81xe7T-S2bL._SL1500_.jpg",
                "thumb": "https://m.media-amazon.com/images/I/81xe7T-S2bL._SS40_.jpg",
                "large": "https://m.media-amazon.com/images/I/81xe7T-S2bL.jpg",
                "variant": "MAIN"
            }
        ],
        "videos": [],
        "store": "LEGO",
        "categories": [],
        "details": {
            "Color": "Multi",
            "Size": "Large",
            "Material": "Plastic",
            "Brand": "LEGO",
            "Style": "Star Wars",
            "Product Dimensions": "12 x 10 x 6 inches; 1.2 pounds",
            "UPC": "673419292631",
            "Manufacturer": "LEGO"
        },
        "parent_asin": "B07H8Y2W6X",
        "bought_together": None
    },
    {
        "id": 5,
        "main_category": "Sports & Outdoors",
        "title": "Fitbit Charge 5 Fitness and Health Tracker",
        "average_rating": 4.6,
        "rating_number": 4000,
        "features": [
            "Built-in GPS for real-time pace and distance.",
            "Tracks heart rate, sleep, and stress levels.",
            "Sleep Score, SpO2, and ECG for health insights.",
            "Long battery life of up to 7 days.",
            "Water-resistant up to 50 meters."
        ],
        "description": [
            "Description",
            "The Fitbit Charge 5 is a fitness and health tracker that offers comprehensive health insights, including heart rate, sleep, stress, and SpO2 tracking. It features a built-in GPS, long battery life, and water resistance.",
            "Feature",
            "- Color: Black.- Material: Plastic.- Size: 1.2 x 1.6 x 0.5 inches.",
            "Package Including",
            "1 x Fitbit Charge 5 Fitness Tracker, 1 x Charging Cable, 1 x User Manual"
        ],
        "price": 129.95,
        "images": [
            {
                "hi_res": "https://m.media-amazon.com/images/I/71kHgGZbllL._SL1500_.jpg",
                "thumb": "https://m.media-amazon.com/images/I/71kHgGZbllL._SS40_.jpg",
                "large": "https://m.media-amazon.com/images/I/71kHgGZbllL.jpg",
                "variant": "MAIN"
            }
        ],
        "videos": [],
        "store": "Fitbit",
        "categories": [],
        "details": {
            "Color": "Black",
            "Size": "Small",
            "Material": "Plastic",
            "Brand": "Fitbit",
            "Style": "Fitness Tracker",
            "Product Dimensions": "1.2 x 1.6 x 0.5 inches; 0.2 pounds",
            "UPC": "811138034248",
            "Manufacturer": "Fitbit"
        },
        "parent_asin": "B097WNBF2H",
        "bought_together": None
    },
    {
        "id": 6,
        "main_category": "Clothing & Accessories",
        "title": "Columbia Men’s Watertight II Jacket",
        "average_rating": 4.8,
        "rating_number": 2200,
        "features": [
            "Waterproof and breathable technology.",
            "Packable and lightweight for easy travel.",
            "Adjustable hood and cuffs for a custom fit.",
            "Multiple zippered pockets for storage.",
            "Available in a variety of colors and sizes."
        ],
        "description": [
            "Description",
            "The Columbia Watertight II jacket is perfect for outdoor adventures. It features waterproof and breathable fabric, adjustable hood and cuffs, and is packable for easy storage.",
            "Feature",
            "- Color: Black.- Material: Nylon.- Size: Small.",
            "Package Including",
            "1 x Columbia Watertight II Jacket"
        ],
        "price": 89.99,
        "images": [
            {
                "hi_res": "https://m.media-amazon.com/images/I/91l28e1w8LL._SL1500_.jpg",
                "thumb": "https://m.media-amazon.com/images/I/71mCm9ezYvL._SS40_.jpg",
                "large": "https://m.media-amazon.com/images/I/71mCm9ezYvL.jpg",
                "variant": "MAIN"
            }
        ],
        "videos": [],
        "store": "Columbia",
        "categories": [],
        "details": {
            "Color": "Black",
            "Size": "Small",
            "Material": "Nylon",
            "Brand": "Columbia",
            "Style": "Rain Jacket",
            "Product Dimensions": "12 x 9 x 2 inches; 1.5 pounds",
            "UPC": "887921729721",
            "Manufacturer": "Columbia"
        },
        "parent_asin": "B07K3D2CV7",
        "bought_together": None
    }
]


def get_products(db: Session, username: str, if_fake_data: bool = False):
    if if_fake_data:
        return [ProductModel(**product) for product in products_test]
    print(username)
    product_for_user = db.query(Users.product_for_user).filter(Users.username == username).first()[0]
    print('#######', product_for_user)
    return [item for item in db.query(ProductModel).filter(ProductModel.parent_asin.in_(product_for_user)).limit(10).all()]

def create_user(username:str, name: str, email: str, phone: str) -> bool:

    try:
        # Exemple : simulation d'une insertion dans une base de données
        print(f"Saving data: Name = {name}, Email = {email}, Phone = {phone}")
        
        # Retourner True si l'enregistrement est réussi
        return True
    except Exception as e:
        print(f"Error while saving user data: {e}")
        return False

def user_exist(db: Session, username: str):
    return db.query(Users).filter(Users.username == username).first is not None

def get_answer_bot(db: Session, conversation: list[dict], username: str, cart: dict):
    user = db.query(Users).filter(Users.username == username).first()
    print("#######fdsq", type(user))
    
    # Récupérer la réponse et les parent_asin_ids
    reponse, parent_asin_ids = get_response(user, conversation, cart, "")
    
    # Si la liste de produits pour l'utilisateur existe déjà
    if user.product_for_user is None :
        user.product_for_user = parent_asin_ids
    else:
        if len(parent_asin_ids)>0:
            user.product_for_user = parent_asin_ids

    # Sauvegarder les changements dans la base de données
    db.commit()
    
    return reponse, "/"