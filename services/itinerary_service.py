from models import db, Itinerary, ItineraryDay
from services.location_service import LocationService
import random

class ItineraryService:
    @staticmethod
    def get_all_itineraries():
        """Get all itineraries ordered by creation date descending"""
        return Itinerary.query.order_by(Itinerary.created_date.desc()).all()

    @staticmethod
    def get_itinerary_by_id(itinerary_id):
        """Get a single itinerary by ID"""
        return Itinerary.query.get(itinerary_id)

    @staticmethod
    def create_itinerary(title, location, duration):
        """Create a new itinerary with location-specific activities"""
        new_itinerary = Itinerary(title=title, location=location, duration=duration, activities="")
        db.session.add(new_itinerary)
        db.session.flush()  # Get the ID without committing

        # Get location-specific data
        location_data = LocationService.get_location_data(location)
        attractions = location_data.get('attractions', [])
        restaurants = location_data.get('restaurants', [])

        # Generate day-wise activities with specific locations
        day_activities = ItineraryService._generate_location_based_activities(
            location, duration, attractions, restaurants
        )

        # Create itinerary days
        for day_num in range(1, duration + 1):
            day_data = day_activities.get(day_num, {
                "morning": "Explore {}".format(location),
                "afternoon": "Visit local attractions in {}".format(location),
                "evening": "Relax and enjoy {}".format(location)
            })

            itinerary_day = ItineraryDay(
                itinerary_id=new_itinerary.id,
                day_number=day_num,
                morning=day_data.get("morning", "Explore"),
                afternoon=day_data.get("afternoon", "Sightsee"),
                evening=day_data.get("evening", "Relax"),
                notes=day_data.get("notes", "")
            )
            db.session.add(itinerary_day)

        db.session.commit()
        return new_itinerary

    @staticmethod
    def _generate_location_based_activities(location, duration, attractions, restaurants):
        """Generate specific activities based on location data"""
        activities = {}

        # Shuffle attractions to provide variety
        available_attractions = attractions[:]
        random.shuffle(available_attractions)

        # Shuffle restaurants
        available_restaurants = restaurants[:]
        random.shuffle(available_restaurants)

        attraction_index = 0
        restaurant_index = 0

        for day in range(1, duration + 1):
            day_activities = {}

            # Morning: Visit an attraction
            if attraction_index < len(available_attractions):
                attraction = available_attractions[attraction_index]
                day_activities["morning"] = "Visit {} - {}".format(attraction['name'], attraction['description'])
                attraction_index += 1
            else:
                day_activities["morning"] = "Explore local attractions in {}".format(location)

            # Afternoon: Another attraction or activity
            if attraction_index < len(available_attractions):
                attraction = available_attractions[attraction_index]
                day_activities["afternoon"] = "Visit {} - {}".format(attraction['name'], attraction['description'])
                attraction_index += 1
            else:
                day_activities["afternoon"] = "Enjoy leisure activities in {}".format(location)

            # Evening: Restaurant or cultural activity
            if restaurant_index < len(available_restaurants):
                restaurant = available_restaurants[restaurant_index]
                day_activities["evening"] = "Dinner at {} - {} cuisine".format(restaurant['name'], restaurant['cuisine'])
                restaurant_index += 1
            else:
                day_activities["evening"] = "Experience local culture and cuisine in {}".format(location)

            # Add special notes for certain locations
            notes = ItineraryService._get_location_notes(location, day, duration)
            if notes:
                day_activities["notes"] = notes

            activities[day] = day_activities

        return activities

    @staticmethod
    def _get_location_notes(location, day, total_days):
        """Get special notes for specific locations and days"""
        notes = []

        # Location-specific tips
        if location == "Goa":
            if day == 1:
                notes.append("Don't forget sunscreen and comfortable walking shoes for beach activities")
            if day == total_days:
                notes.append("Consider buying spices and cashews from local markets as souvenirs")

        elif location == "Kerala":
            if day == 1:
                notes.append("Book houseboat in advance during peak season")
            notes.append("Try traditional Kerala dishes like appam with fish curry")

        elif location == "Rajasthan":
            notes.append("Respect local customs and dress modestly when visiting temples")
            if day == 1:
                notes.append("Stay hydrated and wear comfortable shoes for fort explorations")

        elif location == "Himachal Pradesh":
            notes.append("Carry warm clothing as temperatures can drop significantly")
            if day <= 2:
                notes.append("Acclimatize to high altitude gradually")

        elif location == "Uttarakhand":
            if day == 1:
                notes.append("Visit early morning for peaceful Ganges darshan")
            notes.append("Respect spiritual sites and maintain silence")

        elif location == "Mumbai":
            notes.append("Use local trains for authentic experience (but be careful with belongings)")
            if day == 1:
                notes.append("Try street food from reliable vendors")

        elif location == "Delhi":
            notes.append("Bargain politely at markets and always agree on prices beforehand")
            if day == 1:
                notes.append("Start with Red Fort early morning to avoid crowds")

        elif location == "Agra":
            if day == 1:
                notes.append("Book Taj Mahal tickets online in advance")
            notes.append("Visit Taj Mahal at sunrise for magical experience")

        elif location == "Varanasi":
            notes.append("Wake up early for Ganges aarti ceremony")
            if day == 1:
                notes.append("Take a boat ride at dawn for spiritual experience")

        elif location == "Jaipur":
            if day == 1:
                notes.append("Visit Amber Fort early to see light and sound show")
            notes.append("Try traditional Rajasthani thali for authentic cuisine")

        elif location == "Udaipur":
            notes.append("Take a lake cruise on Lake Pichola in the evening")
            if day == 1:
                notes.append("Visit City Palace early morning")

        elif location == "Pondicherry":
            notes.append("Rent a bicycle to explore the French Quarter")
            if day == 1:
                notes.append("Visit Auroville for spiritual experience")

        elif location == "Shimla":
            notes.append("Take the toy train from Kalka for scenic journey")
            if day == 1:
                notes.append("Walk the Mall Road for colonial architecture")

        elif location == "Manali":
            notes.append("Carry ID proof for Rohtang Pass permit")
            if day == 1:
                notes.append("Visit Hadimba Temple for ancient architecture")

        elif location == "Leh Ladakh":
            notes.append("Drink plenty of water to combat high altitude effects")
            if day == 1:
                notes.append("Rest and acclimatize to high altitude")

        elif location == "Kashmir":
            notes.append("Stay on houseboat for authentic experience")
            if day == 1:
                notes.append("Visit Mughal gardens early morning")

        elif location == "Bangalore":
            notes.append("Try filter coffee at local cafes")
            if day == 1:
                notes.append("Visit Lalbagh Botanical Garden")

        elif location == "Chennai":
            notes.append("Visit Marina Beach for evening stroll")
            if day == 1:
                notes.append("Try South Indian breakfast at local hotels")

        elif location == "Kolkata":
            notes.append("Take a tram ride for nostalgic experience")
            if day == 1:
                notes.append("Visit Victoria Memorial early morning")

        elif location == "Ayodhya":
            notes.append("Visit Ram Janmabhoomi Temple with respect")
            if day == 1:
                notes.append("Take blessings at Hanuman Garhi")

        # General tips for all locations
        if day == 1:
            notes.append("Check-in to hotel and freshen up")
        if day == total_days:
            notes.append("Pack souvenirs and prepare for departure")

        return " | ".join(notes) if notes else ""

    @staticmethod
    def update_itinerary_days(itinerary_id, day_updates):
        """Update itinerary days with new activities"""
        itinerary = Itinerary.query.get(itinerary_id)
        if not itinerary:
            return None

        for day in itinerary.days:
            day_key = "day_{}".format(day.day_number)
            if day_key in day_updates:
                updates = day_updates[day_key]
                if 'morning' in updates:
                    day.morning = updates['morning']
                if 'afternoon' in updates:
                    day.afternoon = updates['afternoon']
                if 'evening' in updates:
                    day.evening = updates['evening']
                if 'notes' in updates:
                    day.notes = updates['notes']

        db.session.commit()
        return itinerary

    @staticmethod
    def delete_itinerary(itinerary_id):
        """Delete an itinerary by ID"""
        itinerary = Itinerary.query.get(itinerary_id)
        if itinerary:
            db.session.delete(itinerary)
            db.session.commit()
            return True
        return False