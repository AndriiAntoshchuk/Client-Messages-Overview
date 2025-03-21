import pandas as pd
import matplotlib.pyplot as plt

# Datei laden
data = pd.read_csv("data/raw/probeaufgabe_2025.csv")
print(data.isnull().sum())
data.info()

# Spalte 'created_at' in Datetime-Format umwandeln
data['created_at'] = pd.to_datetime(data['created_at'])
# Neue Spalten hinzufügen
data['weekday'] = data['created_at'].dt.day_name()
data['hour'] = data['created_at'].dt.hour
data = data.sort_values(by='created_at').reset_index(drop=True)
start_date = data['created_at'].min()
end_date = data['created_at'].max()
print(f"Datenzeitraum: {start_date.date()} bis {end_date.date()}")

# Fehlende Nachrichten basierend auf ihrer Kategorief nachfüllen
category_filler = {
    'technical_problem': 'Der Kunde hat ein technisches Problem.',
    'contract_details': 'Der Kunde bittet um Details zu seinem Vertrag.',
    'self_service': 'Der Kunde hat eine Frage zur Selbstbedienung.',
    'termination': 'Der Kunde fragt nach Kündigungsoptionen.',
    'payout': 'Der Kunde hat eine Frage zur Zahlung'
}
data['message'] = data.apply(lambda row: category_filler[row['category']] if pd.isnull(row['message']) else row['message'], axis=1)

# Zeitliche Verteilung der Nachrichten
plt.figure(figsize=(10, 5))
data['created_at'].dt.date.value_counts().sort_index().plot(kind='line')
plt.xlabel("Datum")
plt.ylabel("Anzahl der Nachrichten")
plt.title("Zeitliche Verteilung der Nachrichten")
plt.xticks(rotation=0)
plt.grid()
plt.show()

# Zeitliche Verteilung der Nachrichten in März
march_data = data[data['created_at'].dt.month == 3]
march_daily_counts = march_data['created_at'].dt.date.value_counts().sort_index()
march_dates = pd.to_datetime(march_daily_counts.index)
x_labels = list(range(1, len(march_daily_counts) + 1))
plt.figure(figsize=(10, 5))
plt.bar(x_labels, march_daily_counts.values, color='red')
plt.title("Nachrichten pro Tag im März")
plt.xlabel("Tag")
plt.ylabel("Anzahl der Nachrichten")
plt.xticks(ticks=x_labels, labels=march_dates.day)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Häufigkeitsverteilung der Nachrichtenkategorien pro Tag (11. - 17. März)
march_filtered = data[(data['created_at'].dt.month == 3) &
                      (data['created_at'].dt.day >= 11) &
                      (data['created_at'].dt.day <= 17)]
march_daily_category_counts = march_filtered.groupby([march_filtered['created_at'].dt.date, 'category']).size().unstack().fillna(0)
march_daily_category_counts.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='tab10')
plt.xlabel("Tag")
plt.ylabel("Anzahl der Nachrichten")
plt.title("Häufigkeitsverteilung der Nachrichtenkategorien pro Tag (11. - 17. März)")
plt.legend(title="Kategorie")
plt.xticks(rotation=0)
plt.grid(axis="y")
plt.tight_layout()
plt.show()

# Häufigkeitsverteilung der Kategorien
plt.figure(figsize=(8, 5))
data['category'].value_counts().plot(kind='bar')
plt.xlabel("Kategorie")
plt.ylabel("Anzahl der Nachrichten")
plt.title("Häufigkeitsverteilung der Nachrichtenkategorien")
plt.xticks(rotation=0)
plt.grid(axis="y")
plt.show()

# Nachrichtenverteilung über den Tag
plt.figure(figsize=(8, 5))
data['hour'].value_counts().sort_index().plot(kind='bar')
plt.xlabel("Stunde des Tages")
plt.ylabel("Anzahl der Nachrichten")
plt.title("Nachrichtenverteilung über den Tag")
plt.xticks(rotation=0)
plt.grid(axis="y")
plt.show()


data.to_csv("data/processed/probeaufgabe_2025_filled_messages.csv", index=False)