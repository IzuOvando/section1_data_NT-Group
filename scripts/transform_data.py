import pandas as pd
import uuid
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

# Estas funciones estan generadas aqui como herramientas para los metodos pero en una aplicacion o microservicio
# deberian de estar distibuidas en utils o servicios y clases segun el manejo de cada transformación.


def clean_or_generate_id(value):
    if value is None:
        return uuid.uuid4().hex[:24]
    value_str = str(value).strip()
    if value_str == "" or value_str.lower() == "none" or value_str.lower() == "nan":
        return uuid.uuid4().hex[:24]
    return value_str[:24]


def clean_datetime_column(series):
    return pd.to_datetime(series, format="mixed").dt.strftime("%Y-%m-%d %H:%M:%S")


def fix_and_validate_decimal_16_2(valor):
    try:
        d = Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        d_abs = d.copy_abs()
        integer_part = d_abs.to_integral_value()

        if integer_part.adjusted() >= 14:
            return None
        return float(d)
    except (InvalidOperation, ValueError):
        return None


def transform_data(input_path: str, output_path: str):
    df = pd.read_csv(input_path)

    # Aqui si tuve conflictos con los valores de los amounts ya que venian valores exorbitantes y no sabia como manejarlos
    # Los maneje por logica y si el decimal es muy grande los redondeo para reducirlo
    # En el caso de los numeros enteros si excede 14 cifras pues ya no es logico con respecto a los demas valores y lo retorno como 0 imprimiendo un warning
    def fix_amount(x):
        fixed = fix_and_validate_decimal_16_2(x)
        if fixed is None:
            print(f"Warning: amount inválido {x}, se setea a 0")
            return 0.0
        return fixed

    df["amount"] = df["amount"].apply(fix_amount)

    df["id"] = df["id"].apply(clean_or_generate_id)
    df["company_id"] = df["company_id"].apply(clean_or_generate_id)

    # Aqui convierto todo string pero lo correcto seria saber que valores contiene status ya se con un enum o de alguna otra forma para decartar datos invalidos.
    df["status"] = df["status"].apply(str)

    # Pandas faclita mucho el anejo de fechas para datetime
    # Aunque me encontre con datos que no coincidian con una sola estructura tome la decision de yo escoger una y convertir esos valores a la estructura definida
    df["created_at"] = clean_datetime_column(df["created_at"])
    df["paid_at"] = pd.to_datetime(df["paid_at"], format="mixed", errors="coerce")

    final_columns = [
        "id",
        "name",
        "company_id",
        "amount",
        "status",
        "created_at",
        "paid_at",
    ]
    df = df[final_columns]

    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    transform_data("data/extracted.csv", "data/transformado.csv")
