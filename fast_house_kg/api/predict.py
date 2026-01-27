import joblib
from fastapi import APIRouter
from fast_house_kg.database.schema import HousePredictSchema

scaler = joblib.load('scaler (1).pkl')
model = joblib.load('model (1).pkl')

predict_router = APIRouter(prefix='/predict', tags=['Predict Price'])

@predict_router.post('/')
async def predict_price(house: HousePredictSchema):
    house_dict = house.dict()
    new_neighborhood = house_dict.pop('Neighborhood')
    neighborhood1or_0 = [
        1 if new_neighborhood == 'Blueste' else 0,
        1 if new_neighborhood == 'BrDale' else 0,
        1 if new_neighborhood == 'BrkSide' else 0,
        1 if new_neighborhood == 'ClearCr' else 0,
        1 if new_neighborhood == 'CollgCr' else 0,
        1 if new_neighborhood == 'Crawfor' else 0,
        1 if new_neighborhood == 'Edwards' else 0,
        1 if new_neighborhood == 'Gilbert' else 0,
        1 if new_neighborhood == 'IDOTRR' else 0,
        1 if new_neighborhood == 'MeadowV' else 0,
        1 if new_neighborhood == 'Mitchel' else 0,
        1 if new_neighborhood == 'NAmes' else 0,
        1 if new_neighborhood == 'NPkVill' else 0,
        1 if new_neighborhood == 'NWAmes' else 0,
        1 if new_neighborhood == 'NoRidge' else 0,
        1 if new_neighborhood == 'NridgHt' else 0,
        1 if new_neighborhood == 'OldTown' else 0,
        1 if new_neighborhood == 'SWISU' else 0,
        1 if new_neighborhood == 'Sawyer' else 0,
        1 if new_neighborhood == 'SawyerW' else 0,
        1 if new_neighborhood == 'Somerst' else 0,
        1 if new_neighborhood == 'StoneBr' else 0,
        1 if new_neighborhood == 'Timber' else 0,
        1 if new_neighborhood == 'Veenker' else 0,
    ]
    features = list(house_dict.values()) + neighborhood1or_0
    scaled_data = scaler.transform([features])
    predict = model.predict(scaled_data)[0]
    return {'Price predict': predict}