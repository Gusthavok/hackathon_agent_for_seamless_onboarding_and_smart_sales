README pitch :

L’objectif de ce projet était de révolutionner l’expérience client de la vente d’affaires de running en centralisant sur une unique plateforme le coach sportif, le vendeur spécialisé, l’expert en sciences du sport et le diététicien, tous personnalisés à l’utilisateur et regroupés dans un unique chatbot. 

Ce chatbot, entraîné sur une base de données d’articles scientifiques sur le sport créée par nos soins, est capable de repérer lorsque l’utilisateur ne cherche que des conseils. Il ne lui propose alors pas des produits à acheter, mais lui confectionne plutôt sur mesure des programmes d’entraînement, des conseils de pratique ou encore de gestion des blessures.

Mais ce chatbot est également un vendeur connecté à la base de données de vente. Il détecte lorsque le client a besoin désire acheter un produit, trouve les plus pertinents dans la base, les classe par ordre d’intérêt en utilisant les produits achetés par des utilisateurs similaires, puis les affiche avec leurs photos. L’utilisateur peut ensuite directement interagir avec les produits affichés, pour les ajouter à son panier ou avoir des détails. Lorsque l’utilisateur est intéressé par un produit, le chatbot propose enfin des produits complémentaires à acheter.

Finalement, ce chatbot est intégré à une interface agréable. Lors de la première connexion au site, l’utilisateur se voit posé plusieurs questions pour définir son profil. Lorsqu’un produit est proposé, une image et les informations sur celui-ci s’affichent. L’utilisateur peut l’ajouter au panier et voir son panier.

README scientifique :

Plusieurs éléments scientifiques ont été utilisés dans ce projet :

1)	Pour l’expert en pratique du sport :

Nous avons construit un dataset de Q&A sur des articles scientifiques de pointe sur la course à pied, les techniques d’entraînement, de récupération et d’alimentation ; pour un total de 1592 Q&A.
Nous avons ensuite mis en place une RAG (idéalement nous aurions fait un finetuning) pour piocher dans ces connaissances.

2)	Pour le vendeur :

Nous avons utilisé un dataset récupéré sur internet d’articles Amazon de sport concernant la course à pied (Amazon-Reviews-2023). 
Avec une RAG, le modèle peut explorer 

README technique :

how to setup :

invite de commande : 
cd website

puis creer un environement virtuel : 
 $ conda create -p ./.venv python=3.11
 $ conda activate ./.venv
 $ pip install -r ./requirements.txt
 $ pip install "fastapi[standard]"

le définir comme interpreteur par default du repo

BACKEND : 


1.⁠ ⁠Aller website/backend/app.

2.⁠ ⁠Créer une base de donnée postgresql nommée website_hack_20242311

3. faire un user qui a tous les privilleges sur cette table, nom : 'postgres' mdp : 'patato'

4. run 
python create_initial_data.py

5.⁠ ⁠Lancer le serveur backend : 
 $ python ./api.py

RMQ : il manque des bibliothèque dans le requirements.txt, il faudra en reinstaller. 


FRONTEND : 
1.⁠ ⁠aller dans website/frontend

2.⁠ ⁠créer et activer un environnement virtuel pour Node.js : (je suis plus tout à fait sur de la commande) :
 $ nodeenv env
 $ . env/bin/activate

3.⁠ ⁠récupérer les bons package : 
 $ npm i

4.⁠ ⁠lancer le serveur frontend : 
 $ npm run dev

pour accéder au login : rajouter dans l'URL /login
