from utils import load_excel, validate_data
from services import analyze_transactions
from reports import save_json, save_excel_report


def main():
    input_file = "data/operations.xlsx"
    df = load_excel(input_file)

    if not validate_data(df):
        print("Ошибка: неверный формат данных!")
        return

    stats = analyze_transactions(df)
    save_json(stats, "data/report.json")
    save_excel_report(df, "data/report.xlsx")


if __name__ == "__main__":
    main()
