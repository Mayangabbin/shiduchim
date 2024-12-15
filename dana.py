import pandas as pd
import os
import hashlib

print("Current Working Directory:", os.getcwd())

# File paths
file_path = "responses.csv" # Input CSV file path
updated_file_path = 'responses_with_ids.csv'  # Updated CSV with Response IDs
processed_ids_file = 'processed_ids.txt'  # File to track processed Response IDs

# Load the responses CSV file
responses = pd.read_csv(file_path)

# Define a function to generate a unique Response ID
def generate_response_id(row):
    # Use fields that uniquely identify a response; adjust according to your CSV structure
    unique_string = f"{row['שם פרטי']}{row['שם משפחה']}{row['חותמת זמן']}"  # Example fields
    return hashlib.md5(unique_string.encode()).hexdigest()  # Create a unique hash

# Check if Response ID column already exists; if not, add it
if 'Response ID' not in responses.columns:
    responses['Response ID'] = responses.apply(generate_response_id, axis=1)
    # Save the updated responses with Response IDs
    responses.to_csv(updated_file_path, index=False)
    print(f"Updated CSV saved to {updated_file_path} with Response IDs.")

# Load processed IDs
if os.path.exists(processed_ids_file):
    with open(processed_ids_file, 'r') as file:
        processed_ids = set(file.read().splitlines())
else:
    processed_ids = set()

# Define a function to generate a personalized text
def generate_text(row):
    return rf"""
    {row['שם פרטי']} {row['שם משפחה']}
    מספר הטלפון שלך: {row['מספר הטלפון שלך']}
    תאריך לידה: {row['תאריך לידה']}
    גובה: {row['גובה']}
    
    גדלתי ב{row['איפה גדלת?']}
    כרגע גר ב{row['מקום מגורים נוכחי']}
    למדתי בתיכון ב{row['איפה למדת בתיכון?']}
    בהמשך למדתי ב{row['באיזו ישיבה או מכינה למדת? כמה שנים?']}
    
    תחנות בחיים: {row['תחנות בחיים']}
    עיסוק נוכחי: {row['עיסוק נוכחי']}
    
    תכונות לפחות שמאפיינות אותי:
    {row['4 תכונות לפחות שמאפיינות אותך']}
    
    מי אני מבחינה חברתית וסוג שיח:
    {row['מי אני מבחינה חברתית וסוג שיח..']}
    
    אני {row['אתה יותר ספונטני או מתוכנן?']}, {row['שקט או דומיננטי?']}, {row['אתה בסגנון עירוני או ישובי?']}
    
    בזמני הפנוי אני {row['מה משמח אותך? מה אתה אוהב לעשות? מה אתה עושה בזמן פנוי או חופשות?']}
    
    אידיאלים ושליחות מדבר אלייך?: {row['אידיאלים, שליחות מדבר אלייך?']}
    שאיפות ותכנונים לעתיד: {row['שאיפות ותכנונים לעתיד']}
    
    ספר לנו על הרמה והסגנון התורני שלך:
    {row['ספר לנו על הרמה והסגנון התורני שלך']}
    
    ספר בקווים כלליים על המשפחה שלך:
    {row['ספר בקווים כלליים על המשפחה שלך']}
    
    האם אתה מוכן לשלוח תמונה שלך לבחורה במקרה והיא מעוניינת בכך?:
    {row['האם אתה מוכן לשלוח תמונה שלך לבחורה במקרה והיא מעוניינת בכך? ']}
    
    מספרים לבירורים: {row['מספרים לבירורים']}
    הערות נוספות או מידע שיכול להועיל?:
    {row['הערות נוספות או מידע שיכול להועיל?']}
    
    איזה סגנון בית אתה רוצה לבנות?:
    {row['איזה סגנון בית אתה רוצה לבנות?']}
    
    תכונות שמהותיות וקריטיות לך בבחורה:
    {row['תכונות שמהותיות וקריטיות לך בבחורה']}
    
    וקצת יותר בהרחבה..:
    {row['וקצת יותר בהרחבה..']}
    
    מה אתה מחפש אצל בחורה מבחינה תורנית?:
    {row['מה אתה מחפש אצל בחורה מבחינה תורנית?']}
    
    האם חשובה לך העדה?: {row['האם חשובה לך העדה?']}
    האם יש משהו שאפסול עליו מבחינה חיצונית?: {row['האם יש משהו שאפסול עליו מבחינה חיצונית?']}
    
    לסיכום אם היית צריך לציין בנקודות מהם שלושת הדברים שהכי חשובים לך בבחורה, מה הם?:
    {row['לסיכום אם היית צריך לציין בנקודות מהם שלושת הדברים שהכי חשובים לך בבחורה, מה הם?']}
    
    טווח גילאים רלוונטי: {row['טווח גילאים רלוונטי']}
    אם יש מסקנות מפגישות קודמות מה נכון וטוב לי, ומה פחות, כתוב לנו. זה יועיל בלדייק אותנו.:
    {row['אם יש מסקנות מפגישות קודמות מה נכון וטוב לי, ומה פחות,  כתוב לנו. זה יועיל בלדייק אותנו.']}
    
    משהו נוסף שתרצה להוסיף בהקשר של מה אתה מחפש?:
    {row['משהו נוסף שתרצה להוסיף בהקשר של מה אתה מחפש?']}
    """ 


# Process new responses


new_ids = []
for index, row in responses.iterrows():
    response_id = row['Response ID']
    if response_id not in processed_ids:  # Process only unprocessed responses
        summary = generate_text(row)
        output_file = f"{row['שם פרטי']}_{row['שם משפחה']}_{row['מספר הטלפון שלך']}.txt"
        with open(output_file, 'w', encoding='utf-8') as file:  
            file.write(summary)
        print(f"Profile for {row['שם פרטי']}{row['שם משפחה']}{row['מספר הטלפון שלך']} saved to {output_file}")
        new_ids.append(response_id)

# Update the processed IDs file
if new_ids:
    with open(processed_ids_file, 'a') as file:
        file.write('\n'.join(new_ids) + '\n')

