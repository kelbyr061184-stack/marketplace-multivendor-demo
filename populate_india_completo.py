import os
import django
import sys

# Configurar el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from vehiculos.models import Marca, Modelo

def crear_marcas_y_modelos():
    # ----------------------------------------
    # COCHES (marcas y modelos populares en India)
    # ----------------------------------------
    coches_data = {
        'Maruti Suzuki': ['Swift', 'Baleno', 'Dzire', 'Alto', 'Wagon R', 'Vitara Brezza', 'Ertiga', 'Ciaz', 'S-Cross', 'Ignis', 'XL6', 'Jimny'],
        'Hyundai': ['i10', 'i20', 'Verna', 'Creta', 'Venue', 'Santro', 'Tucson', 'Elantra', 'Kona', 'Aura', 'Grand i10'],
        'Tata': ['Nexon', 'Tiago', 'Altroz', 'Harrier', 'Safari', 'Tigor', 'Punch', 'Hexa', 'Zest'],
        'Mahindra': ['XUV500', 'Scorpio', 'Thar', 'Bolero', 'XUV300', 'Marazzo', 'KUV100', 'Alturas G4', 'TUV300'],
        'Honda': ['City', 'Amaze', 'WR-V', 'Jazz', 'CR-V', 'Civic', 'Accord', 'BR-V'],
        'Toyota': ['Fortuner', 'Innova Crysta', 'Glanza', 'Yaris', 'Camry', 'Corolla', 'Land Cruiser', 'Vellfire'],
        'Renault': ['Kwid', 'Duster', 'Triber', 'Kiger', 'Lodgy', 'Pulse'],
        'Ford': ['EcoSport', 'Figo', 'Endeavour', 'Freestyle', 'Mustang'],
        'Volkswagen': ['Polo', 'Vento', 'Tiguan', 'Taigun', 'Passat'],
        'Nissan': ['Micra', 'Sunny', 'Kicks', 'Terrano', 'Magnite'],
        'Skoda': ['Octavia', 'Rapid', 'Kushaq', 'Superb'],
        'Kia': ['Seltos', 'Sonet', 'Carnival'],
        'MG': ['Hector', 'ZS EV', 'Gloster', 'Astor'],
        'Jeep': ['Compass', 'Wrangler', 'Meridian'],
        'Datsun': ['Redi-Go', 'Go'],
        'Mitsubishi': ['Pajero', 'Outlander', 'Montero'],
        'Fiat': ['Punto', 'Linea', 'Abarth'],
        'Chevrolet': ['Beat', 'Sail', 'Spark', 'Cruze', 'Enjoy'],
        'Audi': ['A3', 'A4', 'Q3', 'Q5', 'Q7', 'A6'],
        'BMW': ['Serie 1', 'Serie 2', 'Serie 3', 'X1', 'X3', 'X5'],
        'Mercedes-Benz': ['Clase A', 'Clase C', 'Clase E', 'GLA', 'GLC', 'GLE'],
        'Jaguar': ['XE', 'XF', 'F-Pace'],
        'Land Rover': ['Range Rover', 'Discovery', 'Evoque'],
        'Volvo': ['XC40', 'XC60', 'XC90'],
        'Porsche': ['Macan', 'Cayenne', 'Panamera'],
    }

    # ----------------------------------------
    # MOTOS (marcas y modelos populares en India)
    # ----------------------------------------
    motos_data = {
        'Hero': ['Splendor', 'HF Deluxe', 'Passion Pro', 'Xtreme', 'Karizma', 'Glamour', 'Super Splendor', 'Destini', 'Maestro'],
        'Honda': ['Activa', 'CB Shine', 'Hornet', 'Unicorn', 'Livo', 'Dio', 'CB200X', 'Highness', 'CB350', 'CBR', 'X-Blade'],
        'Bajaj': ['Pulsar', 'Platina', 'CT 100', 'Avenger', 'Dominar', 'Discover', 'V', 'Boxer'],
        'TVS': ['Apache', 'Jupiter', 'XL100', 'NTorq', 'Raider', 'Radeon', 'Star City'],
        'Royal Enfield': ['Bullet', 'Classic', 'Himalayan', 'Meteor', 'Interceptor', 'Continental GT', 'Hunter'],
        'Yamaha': ['FZ', 'R15', 'MT-15', 'FZS', 'RayZR', 'Fascino', 'Saluto'],
        'Suzuki': ['Access', 'Gixxer', 'Burgman', 'Intruder', 'Hayate', 'Let\'s'],
        'KTM': ['Duke 200', 'Duke 390', 'RC 200', 'RC 390', 'Adventure'],
        'Harley-Davidson': ['Street 750', 'Iron 883', 'Fat Boy', 'Road King'],
        'Mahindra': ['Mojo', 'Gusto', 'Centuro', 'Rodeo', 'Duro'],
        'Jawa': ['Jawa', 'Jawa 42', 'Perak'],
        'Benelli': ['Imperiale', 'TNT', 'TRK'],
        'Triumph': ['Street Twin', 'Bonneville', 'Tiger'],
        'BMW Motorrad': ['G 310 R', 'G 310 GS', 'S 1000 RR'],
        'Ducati': ['Monster', 'Multistrada', 'Scrambler'],
        'Kawasaki': ['Ninja', 'Z', 'Versys'],
    }

    # Crear marcas de coches y sus modelos
    for marca_nombre, modelos in coches_data.items():
        marca, created = Marca.objects.get_or_create(nombre=marca_nombre, tipo='coche')
        if created:
            print(f"Marca de coche creada: {marca_nombre}")
        for modelo_nombre in modelos:
            modelo, created = Modelo.objects.get_or_create(marca=marca, nombre=modelo_nombre, tipo='coche')
            if created:
                print(f"  Modelo de coche creado: {modelo_nombre}")
            else:
                print(f"  Modelo ya existente: {modelo_nombre}")

    # Crear marcas de motos y sus modelos
    for marca_nombre, modelos in motos_data.items():
        marca, created = Marca.objects.get_or_create(nombre=marca_nombre, tipo='moto')
        if created:
            print(f"Marca de moto creada: {marca_nombre}")
        for modelo_nombre in modelos:
            modelo, created = Modelo.objects.get_or_create(marca=marca, nombre=modelo_nombre, tipo='moto')
            if created:
                print(f"  Modelo de moto creado: {modelo_nombre}")
            else:
                print(f"  Modelo ya existente: {modelo_nombre}")

if __name__ == "__main__":
    print("Iniciando población de marcas y modelos de India...")
    crear_marcas_y_modelos()
    print("Proceso completado.")