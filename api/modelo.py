from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente do arquivo bc.env
load_dotenv("bc.env")
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não encontrada no bc.env")

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

# ------------------ MODELOS ------------------

class Usuario(Base):
    __tablename__ = "Usuarios"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    NOME = Column(String(150), nullable=False)
    CPF = Column(String(11), unique=True, nullable=False)
    TELEFONE = Column(String(20))
    EMAIL = Column(String(150), unique=True)
    SENHA = Column(String(255), nullable=False)
    NIVEL = Column(String(50), nullable=False, default="cliente")
    FOTO = Column(String(500), nullable=False, default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3lUXoW_2yUPKkKpFEVGM04gsRowd0vCyXew&s")

    # Relacionamentos
    reservas = relationship("Reserva", back_populates="usuario", cascade="all, delete-orphan")
    propriedades = relationship("Propriedade", back_populates="usuario", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "ID": self.ID,
            "NOME": self.NOME,
            "CPF": self.CPF,
            "TELEFONE": self.TELEFONE,
            "EMAIL": self.EMAIL,
            "SENHA": self.SENHA,
            "NIVEL": self.NIVEL,
            "FOTO": self.FOTO
        }


class Propriedade(Base):
    __tablename__ = "Propriedades"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    LOCAL = Column(String(200), nullable=False)
    PRECO = Column(DECIMAL(12,2), nullable=False)
    QUARTOS = Column(Integer, nullable=False)
    TAMANHO = Column(DECIMAL(10,2), nullable=False)
    IMAGEM = Column(String(1000), nullable=False)

    USUARIO_ID = Column(Integer, ForeignKey("Usuarios.ID"), nullable=False)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="propriedades")
    reservas = relationship("Reserva", back_populates="propriedade", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "ID": self.ID,
            "LOCAL": self.LOCAL,
            "PRECO": float(self.PRECO),
            "QUARTOS": self.QUARTOS,
            "TAMANHO": float(self.TAMANHO),
            "IMAGEM": self.IMAGEM,
            "USUARIO_ID": self.USUARIO_ID,
            "ANUNCIANTE": self.usuario.NOME if self.usuario else None
        }


class Reserva(Base):
    __tablename__ = "Reservas"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    USUARIO_ID = Column(Integer, ForeignKey("Usuarios.ID"), nullable=False)
    PROPRIEDADE_ID = Column(Integer, ForeignKey("Propriedades.ID"), nullable=False)
    PRECO = Column(DECIMAL(12,2), nullable=False)
    DATA_RESERVA = Column(Date, nullable=False)
    FIM_RESERVA = Column(Date, nullable=True)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="reservas")
    propriedade = relationship("Propriedade", back_populates="reservas")

    def to_dict(self):
        return {
            "ID": self.ID,
            "USUARIO_ID": self.USUARIO_ID,
            "PROPRIEDADE_ID": self.PROPRIEDADE_ID,
            "PRECO": float(self.PRECO),
            "DATA_RESERVA": str(self.DATA_RESERVA),
            "FIM_RESERVA": str(self.FIM_RESERVA) if self.FIM_RESERVA else None
        }


# Cria todas as tabelas no banco
def criar_tabelas():
    Base.metadata.create_all(engine)
