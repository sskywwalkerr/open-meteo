from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database.db import Base


class CurrentWeather(Base):
    __tablename__ = "current_weather"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), index=True, nullable=False)
    temperature_2m = Column(Float, nullable=False)
    wind_speed_10m = Column(Float, nullable=False)
    time = Column(TIMESTAMP, nullable=False)

    hourly_forecast = relationship("HourlyForecast", back_populates="current_weather", cascade="all, delete")


class HourlyForecast(Base):
    __tablename__ = "hourly_forecast"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(TIMESTAMP, nullable=False)
    temperature_2m = Column(Float, nullable=False)
    relative_humidity_2m = Column(Integer, nullable=False)
    wind_speed_10m = Column(Float, nullable=False)

    current_weather_id = Column(Integer, ForeignKey("current_weather.id"))
    current_weather = relationship("CurrentWeather", back_populates="hourly_forecast")