from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

conexion = "mysql+mysqlconnector://root:@localhost:3306/tienda_en_linea"
motor = create_engine(conexion)
Session = sessionmaker(bind=motor)