from main import app
from flask import render_template, redirect,request,flash,session,url_for
from models.models import *
from datetime import datetime, timedelta
from sqlalchemy import func


@app.route('/')
def home():
    if 'user_email' in session:
        if session.get('user_role', None) == 'admin':
            lots = ParkingLot.query.all()
            

            spot = ParkingSpot.query.all()
            for lot in lots:
                total_spots = ParkingSpot.query.filter_by(lot_id=lot.id).count()
                occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
                lot.total_spots = total_spots
                lot.occupied_spots = occupied_spots 
            return render_template("home.html", parking_lots=lots,spot=spot)
        else:
            lots = ParkingLot.query.all()
            
            reserve_parking_spot = ReserveParkingSpot.query.filter_by(user_id=session['user_id']).all()
            spot = ParkingSpot.query.all()
            parameter = request.args.get('parameter')
            query = request.args.get('query')

            if query:
                lots = ParkingLot.query.filter(ParkingLot.prime_location_name.ilike(f'%{query}%'))
            elif parameter == 'address':
                lots = ParkingLot.query.filter(ParkingLot.address.ilike(f'%{query}%'))
            elif parameter == 'pincode':
                lots = ParkingLot.query.filter(ParkingLot.pincode.ilike(f'%{query}%'))

            for lot in lots:
                total_spots = ParkingSpot.query.filter_by(lot_id=lot.id).count()
                occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
                lot.total_spots = total_spots
                lot.occupied_spots = occupied_spots 

            
            
            
            return render_template("home.html", parking_lots=lots,reserve=reserve_parking_spot)
            

    else:
        flash("Please Login First!")
        return render_template('home.html')



@app.route('/users')
def users():
    if 'user_email' not in session or session.get('user_role',None) != 'admin':
        flash('Access denied! Admins only.', 'error')
        return redirect(url_for('home'))
    else:
        users = User.query.filter(User.role_id != 1 ).all()
        return render_template('users.html', users=users)



@app.route('/add_parking_lot', methods=['GET', 'POST'])
def add_parking_lot():
    if session.get('user_role') == 'admin':
    
        if request.method == 'GET':
            return render_template('add_parking_lot.html')
        if request.method == 'POST':
            prime_location = request.form.get('location')
            address = request.form.get('address')
            pincode = request.form.get('pincode')
            price = request.form.get('price')
            max_spots = request.form.get('max_spots')
            

            if not prime_location or not address or not pincode or not price or not max_spots:
                flash('All fields are required!', 'error')
                return redirect(url_for('add_parking_lot'))
            
            parking_lot = ParkingLot.query.filter_by(prime_location_name=prime_location).first()
            if parking_lot:
                flash('Parking lot with this prime location already exists!', 'error')
                return redirect(url_for('add_parking_lot'))
            
            new_parking_lot = ParkingLot(
                prime_location_name=prime_location,
                address=address,
                pincode=pincode,
                price=float(price),
                maximum_number_of_spots=int(max_spots),
                
            )
            db.session.add(new_parking_lot)
            db.session.commit()

            parking_spot = ParkingSpot.query.filter_by(lot_id=new_parking_lot.id).first()
            
            
        
            for i in range(new_parking_lot.maximum_number_of_spots):
                spot = ParkingSpot(
                    lot_id=new_parking_lot.id,
                    status='A'  # Initially, all spots are available
                )
                db.session.add(spot)
            
    
            
            db.session.commit()

            flash('Parking lot added successfully!', 'success')
            return redirect(url_for('home'))
    else:
        flash('Access denied! Admins only.', 'error')
        return redirect(url_for('home'))


@app.route('/edit_parking_lot/<int:parking_lot_id>', methods=['GET', 'POST'])
def edit_parking_lot(parking_lot_id):
    if session.get('user_role') == 'admin':
        parking_lot = ParkingLot.query.get(parking_lot_id)
        if not parking_lot:
            flash('Parking lot not found!', 'error')
            return redirect(url_for('home'))

        if request.method == 'GET':
            return render_template('edit_parking_lot.html', parking_lot=parking_lot)

        if request.method == 'POST':
            prime_location = request.form.get('location')
            address = request.form.get('address')
            pincode = request.form.get('pincode')
            price = request.form.get('price')
            max_spots = request.form.get('max_spots')

            if not prime_location or not address or not pincode or not price or not max_spots:
                flash('All fields are required!', 'error')
                return redirect(url_for('edit_parking_lot', parking_lot_id = parking_lot_id))
            
            


            parking_lot.prime_location_name = prime_location
            parking_lot.address = address
            parking_lot.pincode = pincode
            parking_lot.price = float(price)
            parking_lot.maximum_number_of_spots = int(max_spots)

            db.session.commit()

            # update Parking Spot
            spots = ParkingSpot.query.filter_by(lot_id=parking_lot.id).all()
            current_count = len(spots)
            new_count = parking_lot.maximum_number_of_spots

            if new_count > current_count:
                # Add new spots
                for i in range(new_count - current_count):
                    spot = ParkingSpot(
                        lot_id=parking_lot.id,
                        status='A'  # New spots are available
                    )
                    db.session.add(spot)
            elif new_count < current_count:
                # Remove extra spots (preferably only those that are available)
                available_spots = ParkingSpot.query.filter_by(lot_id=parking_lot.id, status='A').limit(current_count - new_count).all()
                for spot in available_spots:
                    db.session.delete(spot)
        

            db.session.commit()


            flash('Parking lot updated successfully!', 'success')
            return redirect(url_for('home'))
    else:
        flash('Access denied! Admins only.', 'error')
        return redirect(url_for('home'))
    

@app.route('/delete_parking_lot/<int:parking_lot_id>', methods=['GET', 'POST'])
def delete_parking_lot(parking_lot_id):
    if session.get('user_role') == 'admin':
        parking_lot = ParkingLot.query.get(parking_lot_id)
        if not parking_lot:
            flash('Parking lot not found!', 'error')
            return redirect(url_for('home'))

        if request.method == 'GET':
            # Show confirmation page or modal
            return render_template('confirm_delete_parking_lot.html', parking_lot=parking_lot)

        if request.method == 'POST':
            # Delete all associated parking spots
            ParkingSpot.query.filter_by(lot_id=parking_lot.id).delete()
            db.session.delete(parking_lot)
            db.session.commit()
            flash('Parking lot deleted successfully!', 'success')
            return redirect(url_for('home'))
    else:
        flash('Access denied! Admins only.', 'error')
        return redirect(url_for('home'))

@app.route('/view_parking_spot/<int:parking_spot_id>', methods=['GET', 'POST'])
def view_parking_spot(parking_spot_id):
    if session.get('user_role') == 'admin':
        parking_spot = ParkingSpot.query.get(parking_spot_id)
        if not parking_spot:
            flash('Parking spot not found!', 'error')
            return redirect(url_for('home'))

        if request.method == 'GET':
            return render_template('view_parking_spot.html', parking_spot=parking_spot)

        if request.method == 'POST':
            # Delete the parking spot
            db.session.delete(parking_spot)
            db.session.commit()
            flash('Parking spot deleted successfully!', 'success')
            return redirect(url_for('home'))
    else:
        flash('Access denied! Admins only.', 'error')
        return redirect(url_for('home'))
    
@app.route('/reserve_parking_spot/<int:spot_id>', methods=['GET'])
def reserve_parking_spot(spot_id):
    if 'user_email' not in session:
        flash('Please log in to reserve a parking spot.', 'error')
        return redirect(url_for('home'))
    
    reserved_parking_spot = ReserveParkingSpot.query.filter_by(spot_id=spot_id).all()
    if not reserved_parking_spot:
        flash('Parking spot not found!', 'error')
        return redirect(url_for('home'))
    
    
    return render_template('reserve_parking_spot.html', reserved_parking_spot=reserved_parking_spot)

@app.route('/book_parking_spot/<int:lot_id>', methods=['GET', 'POST'])
def book_parking_spot(lot_id):
    if 'user_email' not in session:
        flash('Please log in to book a parking spot.', 'error')
        return redirect(url_for('login')) # Redirect to login page

    # Get the specific spot the user clicked on
    spot = ParkingSpot.query.get(lot_id)

    parking_lot = ParkingLot.query.get_or_404(lot_id)
    available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()

    # Validate the spot
    if not available_spot:
        flash('Parking spot not found!', 'error')
        return redirect(url_for('home'))
    

    # Get the parent parking lot using the relationship
    parking_lot = ParkingLot.query.get(available_spot.lot_id)
    parking_timestamp = datetime.now()


    if request.method == 'GET':
        # Pass the specific spot and its lot to the template
        return render_template('book_parking_spot.html', spot=available_spot, parking_lot=parking_lot,parking_timestamp=parking_timestamp)

    if request.method == 'POST':
        vehicle_no = request.form.get('vehicle_no')
        duration_str = request.form.get('duration') # Duration in hours
        

        if not vehicle_no or not duration_str:
            flash('Vehicle number and duration are required!', 'error')
            return redirect(url_for('book_parking_spot', lot_id=lot_id))

        try:
            duration_hours = int(duration_str)
            if duration_hours <= 0:
                raise ValueError
        except ValueError:
            flash('Please enter a valid, positive number for the duration.', 'error')
            return redirect(url_for('book_parking_spot', lot_id=lot_id))

        # Create the new reservation
        new_reservation = ReserveParkingSpot(
            spot_id=available_spot.id,
            lot_id=parking_lot.id,
            vehicle_no=vehicle_no,
            address = parking_lot.address,
            pincode = parking_lot.pincode,
            user_id=session['user_id'], # Get user_id from the session
            parking_timestamp=parking_timestamp,
            leaving_timestamp=None,
            parking_cost =parking_lot.price/60 # Get price from the lot
        )


        # Update the spot's status to 'Occupied'
        available_spot.status = 'O'
        
        db.session.add(new_reservation)
        db.session.commit()

        flash('Parking spot booked successfully!', 'success')
        return redirect(url_for('home'))



@app.route("/release_parking/<int:reservation_id>", methods=['GET', 'POST'])
def release_parking(reservation_id):
    if 'user_email' not in session:
        flash('Please log in to release a parking spot.', 'error')
        return redirect(url_for('home'))
    reservation = ReserveParkingSpot.query.get(reservation_id)
    if not reservation:
        flash('Reservation not found!', 'error')
        return redirect(url_for('home'))
    
    release_time_str = request.form.get('release_timestamp')
    # release_time = datetime.strptime(release_time_str, '%Y-%m-%dT%H:%M') if release_time_str else datetime.now()
    reservation.leaving_timestamp = datetime.now()
    # print(reservation.leaving_timestamp)

    time_diff = reservation.leaving_timestamp - reservation.parking_timestamp
    
    min = time_diff.total_seconds() / 60
    cost = round(min,2)*reservation.parking_cost
    int(cost)
    # charged_hours = int(hours) + (1 if hours % 1 > 0 else 0)  # Round up partial hour
    # total_cost = charged_hours * float(reservation.parking_cost)

    if request.method == 'GET':
        return render_template('release_parking.html', reserve=reservation,cost=cost)
    if request.method == 'POST':
        # Update the parking spot status to 'Available'
        spot = ParkingSpot.query.get(reservation.spot_id)

        

        if spot:
            spot.status = 'A'
            db.session.commit()

            

        
            # After releasing the spot, reserving time showed in user.dashboard and release button convert into 'Parked Out'
            # reservation.leaving_timestamp = release_time
            reservation.parking_cost = cost
            db.session.commit()
            
            flash('Parking spot released successfully!', 'success')
            return redirect(url_for('home'))


    

@app.route('/edit_profile/<int:user_id>', methods=['GET', 'POST'])
def edit_profile(user_id):
    if 'user_email' not in session:
        flash('Please log in to edit your profile.', 'error')
        return redirect(url_for('home'))
    
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'GET': 
        return render_template('edit_profile.html', user = user)
    
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        pincode = request.form.get('pincode')

        if not name or not address or not pincode:
            flash('All fields are required!', 'error')
            return redirect(url_for('edit_profile', user_id=user_id))
        
        user.user_name = name
        user.user_address = address
        user.user_pincode = pincode

        db.session.commit()
        flash('Profile updated successfully!', 'success')

        return redirect(url_for('home'))
    


@app.route('/summary_admin', methods=['GET'])
def summary_admin():
    if 'user_email' not in session or session.get('user_role', None) != 'admin':
        flash('Access denied! Admins only.', 'error')
        return redirect(url_for('home'))

    reserve_parking_spots = ReserveParkingSpot.query.all()
    # --- Bar Chart Data: Revenue per parking lot (Manual Aggregation) ---

    revenue_labels = []
    revenue_values = []

    parking_lots = ParkingLot.query.all()

    for lot in parking_lots:
        reservations = ReserveParkingSpot.query.filter_by(lot_id=lot.id).all()
        costs = [r.parking_cost for r in reservations]
        

        total_revenue = sum([c or 0 for c in costs])
        revenue_labels.append(lot.prime_location_name)
        revenue_values.append(total_revenue)

    # If no data, fallback to default
    if not revenue_labels:
        revenue_labels = ['No Data']
        revenue_values = [0]


        

    # --- Pie Chart Data: Available vs Occupied ---
    
    total_spots = ParkingSpot.query.count()
    occupied_spots = ParkingSpot.query.filter_by(status='O').count()

    available_spots = total_spots - occupied_spots

    pie_labels = ['Available', 'Occupied']
    pie_values = [available_spots, occupied_spots]

    return render_template(
        'summary_admin.html',
        reserve_parking_spots=reserve_parking_spots,
        revenue_labels=revenue_labels,
        revenue_values=revenue_values,
        pie_labels=pie_labels,
        pie_values=pie_values
    )


@app.route('/summary_user', methods=['GET'])
def summary_user():
    if 'user_email' not in session:
        flash('Please log in to view your summary.', 'error')
        return redirect(url_for('home'))
    user_id = session.get('user_id')
    if not user_id:
        flash('User ID not found in session.', 'error')
        return redirect(url_for('home'))
    reserve_parking_spots = ReserveParkingSpot.query.filter_by(user_id=user_id).all()
    #Duration and Cost Calculation according to reservation_id
    duration = {}
    usage_count = {}

    for reservation in reserve_parking_spots:
        if reservation.leaving_timestamp:
            time_diff = reservation.leaving_timestamp - reservation.parking_timestamp
            
            minutes = int(time_diff.total_seconds() / 60)  # Rounded down to nearest minute
            duration[reservation.id] = minutes
            
            # reservation.parking_cost = total_cost
        else:
            duration[reservation.id] = 'Ongoing'
            reservation.parking_cost = 0

    spot_usage_query = db.session.query(
        ReserveParkingSpot.spot_id, 
        func.count(ReserveParkingSpot.id).label('usage_count')
    ).filter_by(user_id=user_id).group_by(ReserveParkingSpot.spot_id).all()

    # Prepare data for Chart.js
    spot_labels = [f"Spot-{result.spot_id}" for result in spot_usage_query]
    spot_usage_counts = [result.usage_count for result in spot_usage_query]
    print("--- CHART DATA ---")
    print("Labels being sent to template:", spot_labels)
    print("Values being sent to template:", spot_usage_counts)
    print("--------------------")

    # If no reservations, show a message
    if not reserve_parking_spots:
        flash('No reservations found for this user.', 'info')
        return redirect(url_for('home'))
    
    # Create Bar Graph for Summary on already used parking spot
    
    

    usage_labels = list(usage_count.keys())
    usage_values = list(usage_count.values())
    return render_template(
        'summary_user.html',
        reserve_parking_spots=reserve_parking_spots,
        user_id=user_id,duration=duration,usage_labels=spot_labels,
        usage_values=spot_usage_counts)
