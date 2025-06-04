from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="책의 장르를 입력하세요.")

    #genre string 처리
    def __str__(self): #자기 이름을 반환하는 함수
        return self.name

from django.urls import reverse

class Book(models.Model):
    title = models.CharField(max_length=200) #책 제목
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True) #작가이름

    #author를 ForeignKey 사용해준다. 작가는 여러명일 수 없어서.
    summary = models.TextField(max_length=1000, help_text="책의 줄거리를 입력하세요.") #줄거리 입력

    #책 보관을 위한 고유번호 ISBM
    isbn = models.CharField('ISBN', max_length=13, help_text="ISBN을 입력하세요")

    #ManyToManyField를 사용해서 장르가 여러 book들을 포함할 수 있게 한다.
    genre = models.ManyToManyField(Genre, help_text="책 장르를 선택하세요.")

    #book string 처리
    def __str__(self):
        return self.title
    
    #book 레코드에 접근할 수 있는 url를 return
    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])
    
import uuid
from django.contrib.auth.models import User
from datetime import date

class BookInstance(models.Model): #책을 빌려가면 책의 복사본
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200) #출판사
    due_back = models.DateField(null=True, blank=True) #언제 돌려받을지
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = ( #대출상태
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField( #책의 정보
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    #메타 데이터로 반납일자 사용
    class Meta:
        ordering = ['due_back']
    
    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
class Author(models.Model): #작가모델
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    #연체 여부를 알려주는 함수
    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)

    #메타 데이터로 이름을 사용
    class Meta:
        ordering = ['last_name', 'first_name']

    def get_adsolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'