from type_annotations import Categories

TRANSACTION_DESCIPTION_TO_CATEGORY: dict[str, Categories] = {
    # Groceries
    'Costco': Categories.Groceries,
    'STEWLEONARD': Categories.Groceries,
    #Miscellaneous
    'Amazon': Categories.Miscellaneous,
    'COSTCO *ANNUAL RENEWAL': Categories.Miscellaneous,
    #Insurance
    'USAA': Categories.Insurance,

    #Subscriptions
    'AAA MEMBERSHIP DUES': Categories.Subscriptions,
    'CrunchyRoll':  Categories.Subscriptions,
    'Obsidian': Categories.Subscriptions,
    'Apple': Categories.Subscriptions,
    'Spotify': Categories.Subscriptions,
    'COSTCO *Annual Renewal': Categories.Subscriptions,

    # Guilt Free
    'Teng and Sons': Categories.GuiltFree,

    # Transportation
    'Shell OIL': Categories.Transportation
}