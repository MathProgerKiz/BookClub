from books.models import Book


# def rating_update(obj: Book,rating):
#     """Метод для обновления рейтинга книги после отзыва"""
#     if obj.favorited_by is not None:
#         rating_array = list(obj.favorited_by)
#         rating_sum = sum(rating_array)
#         rating_count = len(rating_array)
#         obj.average_rating = rating_sum / rating_count
#     else:
#         obj.average_rating=rating

def rating_update(book: Book, new_rating):
    """Метод для обновления рейтинга книги после отзыва"""
    # Получаем все отзывы на книгу
    reviews = book.reviews.all()
    if reviews.exists():
        # Вычисляем сумму всех рейтингов
        rating_sum = sum(review.rating for review in reviews)
        rating_count = reviews.count()
        # Обновляем средний рейтинг
        book.average_rating = rating_sum / rating_count
    else:
        # Если нет отзывов, устанавливаем рейтинг как новый рейтинг
        book.average_rating = new_rating

    book.save()  # Не забываем сохранить изменения в базе данных

