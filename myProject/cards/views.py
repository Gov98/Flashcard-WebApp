import json
import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import base64
from django.http import HttpResponse
from openai import OpenAI
from datetime import datetime, timedelta

# Import the necessary modules for image processing
from PIL import Image
import io

# Paths to JSON files
CATEGORY_FILE = os.path.join(os.path.dirname(__file__), '../../data/categories.json')
CARD_FILE = os.path.join(os.path.dirname(__file__), '../../data/cards.json')

# Utility functions to read and write JSON data
def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# View for the home page
def home(request):
    return render(request, 'cards/home.html')

# Add views for the learning section
def learning(request):
    categories = read_json(CATEGORY_FILE)['Category']
    cards_data = read_json(CARD_FILE)['flashcards']
    categories_with_count = []
    for category in categories:
        category_id = category['Category_Id']
        category_name = category['Category_Name']
        category_desc = category['Category_Desc']
        
        # Find the number of cards for the current category
        num_cards = sum(len(cat['Cards']) for cat in cards_data if cat['Category_Id'] == category_id)
        # Append category details with card count to the list
        categories_with_count.append({
            'Category_Id': category_id,
            'Category_Name': category_name,
            'Category_Desc': category_desc,
            'No_Of_Cards': num_cards
        })
    return render(request, 'cards/learning.html', {'categories': categories_with_count})

def study_flashcards(request, category_id):
    print("study_flashcards")
    category_id = int(category_id)
    cards_data = read_json(CARD_FILE)
    selected_category = next((cat for cat in cards_data['flashcards'] if cat['Category_Id'] == category_id), None)
     # Convert image paths to URLs
    if selected_category:
        two_days_ago = datetime.now() - timedelta(days=2)
        filtered_cards = []
        for card in selected_category['Cards']:
            last_correct_guess = card.get('Last_Correct_Guess')
            if last_correct_guess:
                last_correct_guess = datetime.fromisoformat(last_correct_guess)
                if last_correct_guess < two_days_ago:
                    filtered_cards.append(card)
            else:
                filtered_cards.append(card)
        length=len(filtered_cards)
        print(length)
        selected_category['Cards'] = filtered_cards

        for card in selected_category['Cards']:
            if card['Path']:
                with open(card['Path'], 'rb') as img_file:
                    img_data = img_file.read()
                # Encode the image data as base64
                card['Image_Base64'] = base64.b64encode(img_data).decode('utf-8')
        selected_category["Length"]=length
        print(selected_category)
    return render(request, 'cards/study_flashcards.html', {'category_id':category_id,'category': selected_category})

def mark_correct_guess(request):
    print("mark_correct_guess")
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        cat_id=data.get('category_id')
        print(cat_id)
        card_id = data.get('card_id')
        result = data.get('result')  # 'correct' or 'wrong'
        # Load the cards JSON
        cards_data = read_json(CARD_FILE)['flashcards']

        # Find the card and update the Last_Correct_Guess timestamp
        for category in cards_data:
            if category['Category_Id']==cat_id:
                for card in category['Cards']:
                    if card['Card_Id'] == card_id:
                        # Update Last_Correct_Guess if correct
                        if result == 'correct':
                            card['Last_Correct_Guess'] = datetime.now().isoformat()
                        
                        # Update Learning_History
                        if 'Learning_History' not in card:
                            card['Learning_History'] = []
                        
                        card['Learning_History'].append({
                            'result': result,
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        # Keep only the last 5 entries
                        card['Learning_History'] = card['Learning_History'][-5:]
                        
                        break
        # Save the updated JSON
        write_json(CARD_FILE, {'flashcards': cards_data})
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid request'}, status=400)


# View for creating a category
def create_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_desc = request.POST.get('category_desc')

        categories = read_json(CATEGORY_FILE)
        category_id = len(categories['Category']) + 1
        new_category = {
            "Category_Id": category_id,
            "Category_Name": category_name,
            "Category_Desc": category_desc
        }
        categories['Category'].append(new_category)
        write_json(CATEGORY_FILE, categories)
        
        return redirect('home')
    return render(request, 'cards/create_category.html')

# View for creating a card
def create_card(request):
    categories = read_json(CATEGORY_FILE)['Category']
    if request.method == 'POST':
        category_id = int(request.POST.get('category_id'))
        card_name = request.POST.get('card_name')
        card_desc = request.POST.get('card_desc')
        image = request.FILES.get('image')  # Access the uploaded file
        category_name=[cat['Category_Name'] for cat in categories if cat['Category_Id'] == category_id][0]
        cards = read_json(CARD_FILE)
        flashcards = cards['flashcards']
        category_found = False
        if len(cards['flashcards'])==0:
            card_id=1
        else:
            category_found, card_id = any(a['Category_Id'] == category_id for a in flashcards), max((len(a['Cards']) + 1 if a['Category_Id'] == category_id else 1 for a in flashcards), default=1)
        
         # Save image to local filesystem
        if image:
            image_path = os.path.join(settings.MEDIA_ROOT, f'{category_id}_{card_id}_{image.name}')
            with open(image_path, 'wb') as img_file:
                for chunk in image.chunks():
                    img_file.write(chunk)
        else:
            image_path = None

        new_card = {
            "Card_Id": card_id,
            "Card_Name": card_name,
            "Card_Desc": card_desc,
            "Path": image_path  # Assuming image is saved as a base64 string
        }
        
        for category in flashcards:
            if category['Category_Id'] == category_id:
                category['Cards'].append(new_card)
                break
        else:
            flashcards.append({
                "Category_Id": category_id,
                "Category_Name":category_name,
                "Cards": [new_card]
            })
        try:
            write_json(CARD_FILE, cards)
            response = {'status': 'success', 'message': 'Card Successfully Created'}
        except Exception as e:
            response = {'status': 'error', 'message': 'Card Creation Failed'}       
        
    return render(request, 'cards/create_card.html', {'categories': categories})

# View for managing cards
def manage_cards(request):
    categories = read_json(CATEGORY_FILE)['Category']
    cards_data = read_json(CARD_FILE)['flashcards']
    categories_with_count = []
    for category in categories:
        category_id = category['Category_Id']
        category_name = category['Category_Name']
        category_desc = category['Category_Desc']
        
        # Find the number of cards for the current category
        num_cards = sum(len(cat['Cards']) for cat in cards_data if cat['Category_Id'] == category_id)
        if num_cards>0:
            # Append category details with card count to the list
            categories_with_count.append({
                'Category_Id': category_id,
                'Category_Name': category_name,
                'Category_Desc': category_desc,
                'No_Of_Cards': num_cards
            })
    return render(request, 'cards/manage_cards.html', {'categories': categories_with_count})


# View for displaying cards in a category
def view_category(request, category_id):
    category_id = int(category_id)
    cards = read_json(CARD_FILE)['flashcards']
    selected_category = next((cat for cat in cards if cat['Category_Id'] == category_id), None)

    # Convert image paths to URLs
    if selected_category:
        for card in selected_category['Cards']:
            if card['Path']:
                with open(card['Path'], 'rb') as img_file:
                    img_data = img_file.read()
                # Encode the image data as base64
                card['Image_Base64'] = base64.b64encode(img_data).decode('utf-8')
    return render(request, 'cards/view_category.html', {'category': selected_category})


# View for updating cards in a category
def update_card(request, category_id, card_id):
    print("update_card")
    category_id = int(category_id)
    cards = read_json(CARD_FILE)['flashcards']
    selected_category = next((cat for cat in cards if cat['Category_Id'] == category_id), None)
    if request.method == 'POST':
        card_name = request.POST.get('card_name')
        card_desc = request.POST.get('card_desc')
        image = request.FILES.get('image')

        for card in selected_category['Cards']:
            if card['Card_Id'] == card_id:
                card['Card_Name'] = card_name
                card['Card_Desc'] = card_desc

                # Update the image only if a new image is provided
                if image:
                    image_path = os.path.join(settings.MEDIA_ROOT, f'{category_id}_{card_id}_{image.name}')
                    with open(image_path, 'wb') as img_file:
                        for chunk in image.chunks():
                            img_file.write(chunk)
                    card['Path'] = image_path
                break

        write_json(CARD_FILE, {'flashcards': cards})
        
        return redirect('view_category', category_id=category_id)

    return redirect('view_category', category_id=category_id)

def get_interesting_facts(request):
    print("get_interesting_facts")
    if request.method == "POST":
        print("POST")
        data = json.loads(request.body)
        card_name = data.get("card_name")
        category_name = data.get("category_name")
        client = OpenAI(
            api_key="LL-5Cn6of7n0cxWfuwivcwljNiFHAeEHwr8oLWGfBsL78EB5Oe1NaXIuGB9nFk9unUz",
            base_url="https://api.llama-api.com"
        )

        prompt = f"Give some interesting details about {card_name} in {category_name} as 2 or 3 points(numbered) with each point about 10 words"
        response = client.chat.completions.create(
            model="llama-13b-chat",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        message = response.choices[0].message.content
        return JsonResponse({"message": message})
    else:
        return JsonResponse({"message": "Invalid request method."}, status=400)
    
def view_card(request, category_id, card_id):
    category_id = int(category_id)
    card_id = int(card_id)
    cards_data = read_json(CARD_FILE)['flashcards']
    selected_category = next((cat for cat in cards_data if cat['Category_Id'] == category_id), None)
    selected_card = next((card for card in selected_category['Cards'] if card['Card_Id'] == card_id), None)
    
    if selected_card and selected_card['Path']:
        with open(selected_card['Path'], 'rb') as img_file:
            img_data = img_file.read()
        selected_card['Image_Base64'] = base64.b64encode(img_data).decode('utf-8')
    return render(request, 'cards/view_card.html', {'card': selected_card, 'category_id': category_id})

def submit_score(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        category_id = data.get('category_id')
        score = data.get('score')

        # Update the category's score in cards_data
        category_data = read_json(CATEGORY_FILE)
        for category in category_data['Category']:
            if category['Category_Id'] == category_id:
                if 'Score' not in category:
                    category['Score'] = []
                category['Score'].append(score)
                # Keep only the last 5 scores
                category['Score'] = category['Score'][-5:]
                break
        category_data["recent_score"]=score
        # Save updated cards_data back to the JSON file
        write_json(CATEGORY_FILE,category_data)
        
        return JsonResponse({'status': 'success'})
    print("fininshed")
    return redirect('learning')

def get_recent_score(request):
    categories = read_json(CATEGORY_FILE)
    recent_score = categories["recent_score"]
    print("result")
    print(recent_score)
    return JsonResponse({'recent_score': recent_score})

def get_deck_count(request):
    categories = read_json(CATEGORY_FILE)
    if categories["Category"]:
        leng=len(categories["Category"])
        print(len)
        return JsonResponse({'cat_count': leng})