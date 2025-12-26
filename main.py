"""
Library Book Usage Analytics System
A comprehensive system for tracking and analyzing book usage patterns in libraries.
"""

from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple
import json


class Book:
    """Represents a book in the library."""
    
    def __init__(self, book_id: str, title: str, author: str, isbn: str):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_checkouts = 0
        self.checkout_history = []
        self.last_checkout = None
    
    def record_checkout(self, member_id: str, checkout_date: datetime):
        """Record a book checkout."""
        self.total_checkouts += 1
        self.checkout_history.append({
            'member_id': member_id,
            'checkout_date': checkout_date.isoformat()
        })
        self.last_checkout = checkout_date
    
    def to_dict(self) -> Dict:
        """Convert book to dictionary representation."""
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'total_checkouts': self.total_checkouts,
            'last_checkout': self.last_checkout.isoformat() if self.last_checkout else None
        }


class Member:
    """Represents a library member."""
    
    def __init__(self, member_id: str, name: str, email: str):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.books_checked_out = []
        self.checkout_history = []
    
    def checkout_book(self, book: Book, checkout_date: datetime):
        """Checkout a book."""
        self.books_checked_out.append(book.book_id)
        self.checkout_history.append({
            'book_id': book.book_id,
            'checkout_date': checkout_date.isoformat()
        })
        book.record_checkout(self.member_id, checkout_date)
    
    def return_book(self, book_id: str):
        """Return a book."""
        if book_id in self.books_checked_out:
            self.books_checked_out.remove(book_id)
            return True
        return False
    
    def to_dict(self) -> Dict:
        """Convert member to dictionary representation."""
        return {
            'member_id': self.member_id,
            'name': self.name,
            'email': self.email,
            'books_currently_checked_out': len(self.books_checked_out),
            'total_checkouts': len(self.checkout_history)
        }


class LibraryAnalytics:
    """Analytics engine for library book usage."""
    
    def __init__(self):
        self.books = {}
        self.members = {}
        self.analytics_data = defaultdict(list)
    
    def add_book(self, book: Book) -> bool:
        """Add a book to the library."""
        if book.book_id not in self.books:
            self.books[book.book_id] = book
            return True
        return False
    
    def add_member(self, member: Member) -> bool:
        """Add a member to the library."""
        if member.member_id not in self.members:
            self.members[member.member_id] = member
            return True
        return False
    
    def process_checkout(self, member_id: str, book_id: str, checkout_date: datetime) -> bool:
        """Process a book checkout."""
        if member_id not in self.members or book_id not in self.books:
            return False
        
        member = self.members[member_id]
        book = self.books[book_id]
        member.checkout_book(book, checkout_date)
        return True
    
    def get_most_popular_books(self, limit: int = 10) -> List[Dict]:
        """Get the most popular books by checkout count."""
        sorted_books = sorted(
            self.books.values(),
            key=lambda b: b.total_checkouts,
            reverse=True
        )
        return [book.to_dict() for book in sorted_books[:limit]]
    
    def get_most_active_members(self, limit: int = 10) -> List[Dict]:
        """Get the most active members by checkout count."""
        sorted_members = sorted(
            self.members.values(),
            key=lambda m: len(m.checkout_history),
            reverse=True
        )
        return [member.to_dict() for member in sorted_members[:limit]]
    
    def get_books_by_author(self, author: str) -> List[Dict]:
        """Get all books by a specific author."""
        author_books = [
            book.to_dict() for book in self.books.values()
            if book.author.lower() == author.lower()
        ]
        return author_books
    
    def get_member_checkout_history(self, member_id: str) -> List[Dict]:
        """Get checkout history for a specific member."""
        if member_id not in self.members:
            return []
        
        member = self.members[member_id]
        return member.checkout_history
    
    def get_usage_statistics(self) -> Dict:
        """Get overall library usage statistics."""
        total_books = len(self.books)
        total_members = len(self.members)
        total_checkouts = sum(book.total_checkouts for book in self.books.values())
        avg_checkouts_per_book = (
            total_checkouts / total_books if total_books > 0 else 0
        )
        
        return {
            'total_books': total_books,
            'total_members': total_members,
            'total_checkouts': total_checkouts,
            'average_checkouts_per_book': round(avg_checkouts_per_book, 2),
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def export_analytics_to_json(self, filename: str = 'analytics_report.json'):
        """Export analytics data to JSON file."""
        report = {
            'timestamp': datetime.utcnow().isoformat(),
            'statistics': self.get_usage_statistics(),
            'most_popular_books': self.get_most_popular_books(10),
            'most_active_members': self.get_most_active_members(10)
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filename


def main():
    """Main function to demonstrate the Library Book Usage Analytics System."""
    
    # Initialize the analytics engine
    analytics = LibraryAnalytics()
    
    # Add sample books
    books_data = [
        ('B001', 'The Great Gatsby', 'F. Scott Fitzgerald', '978-0-7432-7356-5'),
        ('B002', '1984', 'George Orwell', '978-0-452-28423-4'),
        ('B003', 'To Kill a Mockingbird', 'Harper Lee', '978-0-06-112008-4'),
        ('B004', 'Pride and Prejudice', 'Jane Austen', '978-0-14-143951-8'),
        ('B005', 'The Catcher in the Rye', 'J.D. Salinger', '978-0-316-76948-0'),
    ]
    
    for book_id, title, author, isbn in books_data:
        book = Book(book_id, title, author, isbn)
        analytics.add_book(book)
    
    # Add sample members
    members_data = [
        ('M001', 'Alice Johnson', 'alice@example.com'),
        ('M002', 'Bob Smith', 'bob@example.com'),
        ('M003', 'Carol Davis', 'carol@example.com'),
    ]
    
    for member_id, name, email in members_data:
        member = Member(member_id, name, email)
        analytics.add_member(member)
    
    # Record sample checkouts
    base_date = datetime(2025, 12, 1)
    checkouts = [
        ('M001', 'B001', datetime(2025, 12, 5)),
        ('M001', 'B002', datetime(2025, 12, 10)),
        ('M002', 'B001', datetime(2025, 12, 6)),
        ('M002', 'B003', datetime(2025, 12, 12)),
        ('M003', 'B004', datetime(2025, 12, 8)),
        ('M001', 'B004', datetime(2025, 12, 15)),
    ]
    
    for member_id, book_id, checkout_date in checkouts:
        analytics.process_checkout(member_id, book_id, checkout_date)
    
    # Display analytics
    print("=" * 60)
    print("LIBRARY BOOK USAGE ANALYTICS SYSTEM")
    print("=" * 60)
    
    print("\n📊 Usage Statistics:")
    stats = analytics.get_usage_statistics()
    for key, value in stats.items():
        if key != 'generated_at':
            print(f"  {key}: {value}")
    
    print("\n📚 Most Popular Books:")
    for i, book in enumerate(analytics.get_most_popular_books(5), 1):
        print(f"  {i}. {book['title']} by {book['author']} ({book['total_checkouts']} checkouts)")
    
    print("\n👥 Most Active Members:")
    for i, member in enumerate(analytics.get_most_active_members(5), 1):
        print(f"  {i}. {member['name']} ({member['total_checkouts']} checkouts)")
    
    # Export report
    report_file = analytics.export_analytics_to_json('library_analytics_report.json')
    print(f"\n✅ Analytics report exported to: {report_file}")
    print("=" * 60)


if __name__ == '__main__':
    main()
