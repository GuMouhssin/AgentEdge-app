import sqlite3
from db.db import connect_db
from .models import Business
import json

def row_to_business(row):
    return Business(
        name=row["name"],
        website=row["website"],
        phone=row["phone"],
        maps_url=row["maps_url"],
        rate=row["rate"],
        contact_page=row["contact_page"],
        emails=json.loads(row["emails"]) if row["emails"] else [],
        facebook=row["facebook"],
        instagram=row["instagram"],
        linkedin=row["linkedin"],
        youtube=row["youtube"],
        status=row["status"],
        lead_score=row["lead_score"]
    )

def insert_business(business):
    conn, cursor = connect_db()
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO businesses (
                name,
                website,
                phone,
                maps_url,
                rate,
                contact_page,
                emails,
                facebook,
                instagram,
                linkedin,
                youtube,
                status,
                lead_score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            business.name,
            business.website,
            business.phone,
            business.maps_url,
            business.rate,
            business.contact_page,
            json.dumps(business.emails),
            business.facebook,
            business.instagram,
            business.linkedin,
            business.youtube,
            business.status,
            business.lead_score
        ))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def get_business_by_url(url):
    conn, cursor = connect_db()
    try:
        cursor.execute("""
            SELECT *
            FROM businesses
            WHERE maps_url = ?
        """, (url,))
        row = cursor.fetchone()
        if row is None:
            return None
        return row_to_business(row)
    finally:
        conn.close()

def get_all_businesses():
    conn, cursor = connect_db()
    try:
        cursor.execute("""
            SELECT *
            FROM businesses
        """)
        rows = cursor.fetchall()
        return [
            row_to_business(row)
            for row in rows
        ]
    finally:
        conn.close()

def get_raw_businesses():
    conn, cursor = connect_db()
    try:
        cursor.execute("""
            SELECT *
            FROM businesses
            WHERE status = 'raw'
        """)
        rows = cursor.fetchall()
        return [
                row_to_business(row) 
                for row in rows
            ]

    finally:
        conn.close()

def delete_business(url):
    conn, cursor = connect_db()
    try:
        cursor.execute('''
            DELETE FROM businesses WHERE maps_url = ?
        ''', (url,))
        conn.commit()
    finally:
        conn.close()

def delete_all_businesses():
    conn, cursor = connect_db()
    try:
        cursor.execute("DELETE FROM businesses")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='businesses'")
        conn.commit()
    finally:
        conn.close()

        
def update_business(business):
    conn, cursor = connect_db()
    try:
        cursor.execute("""
            UPDATE businesses
            SET
                status = ?,
                phone = ?,
                emails = ?,
                contact_page = ?,
                facebook = ?,
                instagram = ?,
                linkedin = ?,
                youtube = ?,
                lead_score = ?
            WHERE maps_url = ?
        """,(
                business.status,
                business.phone,
                json.dumps(business.emails),
                business.contact_page,
                business.facebook,
                business.instagram,
                business.linkedin,
                business.youtube,
                business.lead_score,
                business.maps_url
            )
        )
        conn.commit()
    finally:
        conn.close()



