from bidboard import sg, Bid, Billboard
from sendgrid.helpers.mail import Email, Content, Mail
from flask_login import current_user
import time
import datetime


def send_bid_email(to, bid_id):
    bid = Bid.query.get(bid_id)
    billboard = Billboard.query.get(bid.billboard_id)
    from_email = Email("bids@bidboard.com")
    to_email = Email(to)
    subject = f"Thank You For Placing Your Bid {current_user.first_name}!"
    content = Content(
        "text/html", f"<html><table><tr><td align='center'><img src='https://s3.amazonaws.com/bidboard/11.31851.logo.jpg' height='200px'></td></tr><tr><td>Dear {current_user.first_name} {current_user.last_name},<br><br>You have just place a {bid.amount} MYR bid on BidBoard. The details of your booking are as follows: <br> <br>Billboard size: {billboard.size} <br>Billboard location: {billboard.location} <br>Booking Date and time: {bid.booking_at}<br> <br> This is <b>NOT</b> a confirmed booking. You will recieve another email when the bidding closes to confirm your booking if you are the highest bidder. You will also recieve an email to notify you if someone has outbidded you. <br> Happy Advertising! <br><br>Kind regards, <br> Bidboard Team </td></tr><tr><td align='center'>This is a no-reply address. If you have any questions, please email us <a href='mail=to:ahmed160ramzi@gmail.com'>here.</a></td></tr></table>"
    )

    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())


def send_confirm_email(to, bid_id):
    bid = Bid.query.get(bid_id)
    billboard = Billboard.query.get(bid.billboard_id)
    from_email = Email("booking@bidboard.com")
    to_email = Email(to)
    subject = f"Your Booking Has Been Confirmed {current_user.first_name}!"
    content = Content(
        "text/html", f"<html><table><tr><td align='center'><img src='https://s3.amazonaws.com/bidboard/11.31851.logo.jpg' height='200px'></td></tr><tr><td>Dear {current_user.first_name} {current_user.last_name},<br><br>The bidding has closed and you have been declared the winner! The details of your booking are as follows: <br> <br>Total payment: {bid.amount}<br>Billboard size: {billboard.size} <br>Billboard location: {billboard.location} <br>Booking Date and time: {bid.booking_at}<br> <br>  This is the final confirmation email. We look forward to working with you again!<br> Happy Advertising! <br><br>Kind regards, <br> Bidboard Team </td></tr><tr><td align='center'>This is a no-reply address. If you have any questions, please email us <a href='mail=to:ahmed160ramzi@gmail.com'>here.</a></td></tr></table>"
    )

    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())


def send_outbid_email(to, bid_id, higher_bid_id):
    bid = Bid.query.get(bid_id)
    higher_bid = Bid.query.get(higher_bid_id)
    billboard = Billboard.query.get(bid.billboard_id)
    from_email = Email("bids@bidboard.com")
    to_email = Email(to)
    subject = f"Oh No! Someone Has Outbid You {current_user.first_name}!"
    content = Content(
        "text/html", f"<html><table><tr><td align='center'><img src='https://s3.amazonaws.com/bidboard/11.31851.logo.jpg' height='200px'></td></tr><tr><td>Dear {current_user.first_name} {current_user.last_name},<br><br>Someone has placed a higher bid on one of your booked billboard. The details of the booking are as follows: <br> <br>Your bid: {bid.amount} MYR<br> Highest Bid: {higher_bid.amount} MYR <br>Billboard size: {billboard.size} <br>Billboard location: {billboard.location} <br>Booking Date and time: {bid.booking_at}<br> <br> You still have a chance to get this booking back by raising your bid before {datetime.datetime.fromtimestamp(bid.booking_at)-datetime.timedelta(weeks=-1)}. <br> Happy Advertising! <br><br>Kind regards, <br> Bidboard Team </td></tr><tr><td align='center'>This is a no-reply address. If you have any questions, please email us <a href='mail=to:ahmed160ramzi@gmail.com'>here.</a></td></tr></table>"
    )

    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    # print(response.status_code)
    # print(response.body)
    # print(response.headers)


def send_signup_email(to):
    from_email = Email("signup@bidboard.com")
    to_email = Email(to)
    subject = f"Welcome to Bidboard {current_user.first_name}!"
    content = Content(
        "text/html", f"<html><table><tr><td align='center'><img src='https://s3.amazonaws.com/bidboard/11.31851.logo.jpg' height='200px'></td></tr><tr><td>Dear {current_user.first_name} {current_user.last_name},<br><br>You have just signed up on Bidboard! <br>We encourage you to start browsing our broad collection of billboard locations and sizes. We look forward to working with you on reinforcing and improving your brand recognition and maximising the returns of your marketing campaigns. <br> We wish you the most successful of experiences with Bidboard! <br> <br> Kind regards, <br> Bidboard Team </td></tr><tr><td align='center'>This is a no-reply address. If you have any questions, please email us <a href='mail=to:ahmed160ramzi@gmail.com'>here.</a></td></tr></table>"
    )

    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
