clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
	pip install -e .[dev] --upgrade --no-cache

install:
	pip install -e .['dev']

init_db:
	FLASK_APP=delivery/app.py flask create-db
	FLASK_APP=delivery/app.py flask db upgrade

test:
	FLASK_ENV=test pytest tests/ -v --cov=delivery

format:
	isort **/*.py
	black -l 79 **/*.py

run:
	FLASK_APP=delivery/app.py FLASK_ENV=development flask run

create_categories:
	FLASK_APP=delivery/app.py 
	flask add-category --name=Sorveteria
	flask add-category --name=Lanche
	flask add-category --name=Pizzaria
	flask add-category --name=Pastelaria

create_stores:
	FLASK_APP=delivery/app.py 
	flask add-store --name_store=Chiquinho --user_id=mateus_cardoso44@hotmail.com --category_id=Sorveteria
	flask add-store --name_store="Hora do Lanche" --user_id=mateus_cardoso44@hotmail.com --category_id=Lanche
	flask add-store --name_store="Fera da Lua" --user_id=mateus_cardoso44@hotmail.com --category_id=Pastelaria

create_items:
	FLASK_APP=delivery/app.py 
	flask add-item --name=Pastel --price=5.99 --quantity=10 --description="Carne Moida, Salsicha, Tomate, Batata Palha, Ketchup, Maionese." --store_id="Fera da Lua"
	flask add-item --name=Hamburguer --price=29.99 --quantity=8 --description="Pao brioche, 2 hamburgueres smash de carne suina, creme de cheddar, cebola caramelizada e molho barbecue." --store_id="Hora do Lanche"
	flask add-item --name=Sorvete --price=30.99 --quantity=15 --description="Pote de 950 ml com o nosso autentico Sorvete de Chocolate e pedacos macios de Chocolate Trufado. O Chiquinho no Pote foi feito pra curtir enquanto assiste aquele filminho no aconchego do sofa." --store_id=Chiquinho
	flask add-item --name="Acai" --price=19.99 --quantity=5 --description="Dois deliciosos copos de 480ml, recheados com Acai natural + Granola + Leite condensado + Banana, tudo por um preco especial!" --store_id=Chiquinho

create_everything:
	FLASK_APP=delivery/app.py 
	flask add-category --name=Sorveteria
	flask add-category --name=Lanche
	flask add-category --name=Pizzaria
	flask add-category --name=Pastelaria

	flask add-store --name_store=Chiquinho --user_id=mateus_cardoso44@hotmail.com --category_id=Sorveteria
	flask add-store --name_store="Hora do Lanche" --user_id=mateus_cardoso44@hotmail.com --category_id=Lanche
	flask add-store --name_store="Fera da Lua" --user_id=mateus_cardoso44@hotmail.com --category_id=Pastelaria

	flask add-item --name=Pastel --price=5.99 --quantity=10 --description="Carne Moida, Salsicha, Tomate, Batata Palha, Ketchup, Maionese." --store_id="Fera da Lua"
	flask add-item --name=Hamburguer --price=29.99 --quantity=8 --description="Pao brioche, 2 hamburgueres smash de carne suina, creme de cheddar, cebola caramelizada e molho barbecue." --store_id="Hora do Lanche"
	flask add-item --name=Sorvete --price=30.99 --quantity=15 --description="Pote de 950 ml com o nosso autentico Sorvete de Chocolate e pedacos macios de Chocolate Trufado. O Chiquinho no Pote foi feito pra curtir enquanto assiste aquele filminho no aconchego do sofa." --store_id=Chiquinho
	flask add-item --name="Acai" --price=19.99 --quantity=5 --description="Dois deliciosos copos de 480ml, recheados com Acai natural + Granola + Leite condensado + Banana, tudo por um preco especial!" --store_id=Chiquinho
