from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, TEXT, Boolean, ForeignKey

from myproject.db_config import session, engine, Base


# Определение моделей
class Supplier(Base):
    __tablename__ = 'supplier'
    id = Column(Integer, primary_key=True)
    name = Column(TEXT, nullable=True)
    contact_person = Column(TEXT, nullable=True)
    inn = Column(String(15), nullable=True)
    storage_address = Column(TEXT)
    phone = Column(String(255))
    subscription_cancelled = Column(Boolean, nullable=True, comment="Отписан ли от рассылки")
    subscription_admin = Column(Boolean, nullable=True, comment="Отписан ли от рассылки админом")
    district_id = Column(ForeignKey('district.id'), nullable=True, comment="id области")
    district = relationship('District')

    def __str__(self):
        return f"id: {self.id}  name: {self.name}"


class District(Base):
    __tablename__ = 'district'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, comment="Название области")

    def __str__(self):
        return f"id: {self.id}  name: {self.name}"


class DistrictUtc(Base):
    __tablename__ = 'district_utc'
    id = Column(Integer, primary_key=True)
    district_id = Column(ForeignKey('district.id'), nullable=True, comment="id области")
    district = relationship('District')
    utc = Column(Integer)

    def __str__(self):
        return f"id: {self.id}  district: {self.district} utc: {self.utc}"


# Создание SQLite базы данных
Base.metadata.create_all(engine)

# Создание сессии
# Session = sessionmaker(bind=engine)
# session = Session()

if not session.query(Supplier).first():
    # Заполнение тестовыми данными
    district1 = District(name="Область 1")
    district2 = District(name="Область 2")

    district_utc1 = DistrictUtc(district=district1, utc=3)
    district_utc2 = DistrictUtc(district=district2, utc=5)

    supplier1 = Supplier(
        name="Поставщик 1",
        contact_person="Контакт 1",
        inn="123456789",
        storage_address="Адрес 1",
        phone="1234567890",
        subscription_cancelled=False,
        subscription_admin=False,
        district=district1
    )

    supplier2 = Supplier(
        name="Поставщик 2",
        contact_person="Контакт 2",
        inn="987654321",
        storage_address="Адрес 2",
        phone="0987654321",
        subscription_cancelled=False,
        subscription_admin=False,
        district=district2
    )

    # Добавление данных в сессию
    session.add_all([district1, district2, district_utc1, district_utc2, supplier1, supplier2])

    # Сохранение изменений
    session.commit()

    # Закрытие сессии
    session.close()

    print("Данные успешно добавлены в базу!")
