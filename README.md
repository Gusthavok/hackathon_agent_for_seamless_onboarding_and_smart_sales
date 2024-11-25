LIEN VERS VIDEO DE DEMO : https://drive.google.com/file/d/1c1IU-iX1jSEYFnjgboiQQDguI4L4AQWf/view?usp=sharing 


README pitch :

L’objectif de ce projet était de révolutionner l’expérience client de la vente d’affaires de sport/running en centralisant sur une unique plateforme le coach sportif, le vendeur spécialisé, l’expert en sciences du sport et le diététicien, tous personnalisés à l’utilisateur et regroupés dans un unique chatbot. 

Ce chatbot, entraîné sur une base de données d’articles scientifiques sur le sport créée par nos soins, est capable de repérer lorsque l’utilisateur ne cherche que des conseils. Il ne lui propose alors pas des produits à acheter, mais lui confectionne plutôt sur mesure des programmes d’entraînement, des conseils de pratique ou encore de gestion des blessures. Cela permet de créer un véritable attachement de l'utilisateur à la plateforme, qui n'est plus seulement une plateforme de vente.

Mais ce chatbot est bien sûr également un vendeur connecté à la base de données de vente. Il détecte lorsque le client désire acheter un article, trouve les produits les plus pertinents dans la base, les classe par ordre d’intérêt en utilisant les produits achetés par des utilisateurs similaires, puis les affiche avec leurs photos et descriptions. L’utilisateur peut ensuite directement interagir avec les produits affichés, pour les ajouter à son panier ou avoir des détails. Lorsque l’utilisateur est intéressé par un produit, le chatbot propose également des produits complémentaires à acheter.

Enfin, ce chatbot est intégré à une interface agréable. Lors de la première connexion au site, l’utilisateur se voit posé plusieurs questions pour définir son profil. Lorsqu’un produit est proposé, une image et les informations sur celui-ci s’affichent. L’utilisateur peut l’ajouter au panier et voir son panier.

README démarche scientifique :

Plusieurs éléments scientifiques ont été utilisés dans ce projet :

1)	Pour l’expert en pratique du sport :

Nous avons construit un dataset de Q&A sur des articles scientifiques de pointe sur la course à pied, les techniques d’entraînement, de récupération et d’alimentation.
Pour ce faire, nous avons sélectionné un corpus de 50 articles scientifiques sur le sport, sa pratique et la récupération. Nous avons ensuite généré des questions/réponses avec Mistral small sur ces articles pour un total de 796 Q&A.
Enfin, nous avons utilisé des techniques de data augmentation pour doubler la taille du dataset, pour un total de 1592 Q&A.
Nous avons finalement mis en place une RAG (idéalement nous aurions fait un finetuning) pour piocher dans ces connaissances.

2)	Pour le vendeur :

Nous avons utilisé un dataset récupéré sur internet d’articles Amazon de sport concernant la course à pied (Amazon-Reviews-2023). 
Avec une RAG, le modèle peut explorer la base de données et ses caractéristiques.

Lorsque l'utilisateur cherche un produit, nous utilisons le contexte, la base de données et le profil de l'utilisateur pour trouver des produits cohérents.

Ensuite, nous extrayons ces produits, puis les classons grâce à un algorithme des plus proches voisins : nous regardons quels utilisateurs sont "proches" de notre utilisateur (cette base d'utilisateurs a été créée de façon aléatoire), et nous regardons quels produits ils ont achetés pour donner un score de proximité aux produits proposés par le modèle. Nous combinons enfin ces scores avec le rating ramené à 1 des produits pour faire un score composite qui nous permet de classer les produits (70% score proximité, 30% score rating).

Une fois ces produits classés, nous renvoyons les deux meilleurs au modèle qui les présente avec une description et des détails au modèle. Dans le même temps ces articles sont présentés à gauche. 

A la fin d'une proposition de vente, le modèle propose également des produits complémentaires par prompt-engineering, afin de proposer des options de cross-sales.

3) Pour l'Intent classifier :

Afin de proposer une meilleure expérience client, et pour ne pas que l'utilisateur soit toujouts surchargé d'articles proposés, le modèle doit savoir discriminer entre donner un avis ou proposer des produits. Nous avons utilisé du prompt-engineering pour retoruner un token ou un autre pour ensuite choisir à quel modèle de RAG s'adresser.

4) Pour le site :

Nous avons décidé de créer un vrai site avec différentes pages et des liens entre elles, afin d'éviter de se limiter à une page statique et notamment avoir un accueil nouvel utilisateur et une page panier. En particulier, le chatbot peut naviguer sur le site et interagir avec celui-ci.

5) Points à creuser :

Un regret sur certaines fonctionnalités :
- De nombreux bugs durant l'affichage des produits recommandés du a des problèmes de gestion entre les base de données.
- Pour le moment on ne peut pas créer de nouveau compte utilisateur.  
- La capacité de reprendre la conversation : si un utilisateur parle d'un entraînement au marathon, nous aurions aimé enregistrer le dernier intérêt de l'utilisateur et lui redemander lors de sa connexion suivante par exemple comment son entraînement s'est passé. Cela permettrait de renforcer la sensation de suivi et de personnalisation.
- proposer certaines conditions (taille du panier, produits déjà achetés...) pour que le chatbot propose à l'utilisateur des réductions, afin de renforcer l'aspect commercial personnalisé du chatbot.

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

pour accéder au login : rajouter dans l'URL /login
utiliser un username prédéfini "toto_{x}" pour x entre 0 et 6
