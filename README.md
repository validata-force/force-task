## Setup 
```bash
git clone https://github.com/validata-force/force-task.git
cd force-task
```

```bash
python -m venv .venv
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```
## If you occour Troubleshootion please,

If you encounter build errors with numpy or other packages install packages individually:
```bash
pip install setuptools wheel
pip install Flask==2.3.3 Flask-SQLAlchemy==3.1.1 python-dotenv==1.0.0 pytest==7.4.0 requests==2.31.0
pip install numpy pandas scikit-learn matplotlib seaborn
```

```bash
cd loan_prediction

python train.py
```
```bash
cd ..
python run.py
```
```
http://127.0.0.1:5000
```

## Testings
To run the tests for the bank management system:
```bash
pytest bank_app/tests/test_routes.py
```

## APIs
`/api/banks` `GET`
`/api/banks/<bank_id>` `GET`
 
`/api/banks` `POST`
```json body
{
    "name": "Bank Name",
    "location": "Bank Location"
}
```
- **Response**: Created bank details

`/api/banks/<bank_id>` `PUT`
```json body
{
    "name": "Updated Bank Name",
    "location": "Updated Bank Location"
}
```
 `/api/banks/<bank_id>` `DELETE`

`/loan/api/predict` `POST`
```json body
{
    "income": 70000,
    "credit_score": 720,
    "loan_amount": 20000,
    "loan_term": 48,
    "employment_status": "employed"
}
```
