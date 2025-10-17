from django.db import models, transaction
from django.contrib.auth.models import AbstractUser, Group, Permission







class UserRole(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)

    class Meta:
        db_table = 'user_role'

    def __str__(self):
        return f"{self.username} ({self.role})"
    








class Admins(models.Model):
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Age = models.IntegerField()
    user = models.ForeignKey(
        UserRole,
        on_delete=models.SET_NULL,
        related_name='admins',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'admins'

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.user:
                self.user = UserRole.objects.create_user(
                    username=f"{self.FirstName.lower()}.{self.LastName.lower()}",
                    password='Admin123',
                    role='admin'
                )
            super().save(*args, **kwargs)

    def __str__(self):
        return f"Admin: {self.FirstName} {self.LastName}"
    










class Customers(models.Model):
    CustomerID = models.CharField(unique=True, primary_key=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Age = models.IntegerField()
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
    ]
    Gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    Address = models.CharField(max_length=255)
    City = models.CharField(max_length=100)
    ContactNumber = models.CharField(max_length=15)
    Email = models.EmailField(unique=True)

    user = models.ForeignKey(
        UserRole,
        on_delete=models.SET_NULL,
        related_name='customers',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customers'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
       
        

        with transaction.atomic():
            if not self.user:
                self.user = UserRole.objects.create_user(
                    username=self.Email,
                    email=self.Email,
                    password='defaultpassword',
                    role='user'
                )
            super().save(*args, **kwargs)

            

    def __str__(self):
        return f"Customer: {self.FirstName} {self.LastName} - {self.Email}"
    





class Accounts(models.Model):
    AccountID = models.AutoField(primary_key=True)
    CustomerID = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='accounts', blank=True, null=True)
    AccountType = models.CharField(max_length=50)
    AccountBalance = models.DecimalField(max_digits=10, decimal_places=2)
    DateOfOpening = models.DateTimeField(auto_now_add=True)
    LastTransactionDate = models.DateTimeField(auto_now=True)
    BranchID = models.CharField(max_length=50)

    class Meta:
        db_table = 'accounts'
        ordering = ['-DateOfOpening']

    def __str__(self):
        return f"Account {self.AccountID} - {self.AccountType} - Balance: {self.AccountBalance}"
    







    
class Transactions(models.Model):

    TransactionID = models.CharField(unique=True, primary_key=True)
    AccountID = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='transactions', blank=True, null=True)
    TransactionType = models.CharField(max_length=50)
    TransactionDate = models.DateTimeField(auto_now_add=True)
    TransactionType = models.CharField(max_length=50)
    TransactionAmount = models.DecimalField(max_digits=10, decimal_places=2)
    BalanceAfterTransaction = models.DecimalField(max_digits=10, decimal_places=2)
    Anomaly = models.BooleanField(default=False)

    class Meta:
        db_table = 'transactions'
        ordering = ['-TransactionDate'] 

    def __str__(self):
        return f"Transaction {self.TransactionID} - {self.TransactionType} - Amount: {self.TransactionAmount}"
    










class Loans(models.Model):
    LoanID = models.CharField(unique=True, primary_key=True)
    CustomerID = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='loans', blank=True, null=True)
    LoanType = models.CharField(max_length=50)
    LoanAmount = models.DecimalField(max_digits=10, decimal_places=2)
    InterestRate = models.DecimalField(max_digits=5, decimal_places=2)
    LoanTerm = models.IntegerField()
    ApprovalDate = models.DateTimeField(auto_now_add=True)
    LoanStatus = models.CharField(max_length=50)

    class Meta:
        db_table = 'loans'

    def __str__(self):
        return f"Loan {self.LoanID} - {self.LoanType} - Amount: {self.LoanAmount}"
    








    
class CreditCards(models.Model):
    CardID = models.CharField(unique=True, primary_key=True)
    CustomerID = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='credit_cards', blank=True, null=True)
    CardType = models.CharField(max_length=50)
    CreditLimit = models.DecimalField(max_digits=10, decimal_places=2)
    CreditBalance = models.DecimalField(max_digits=10, decimal_places=2)
    MinimumPaymentDue = models.DecimalField(max_digits=10, decimal_places=2)
    PaymentDueDate = models.DateTimeField()
    LastPaymentDate = models.DateTimeField(null=True, blank=True)
    RewardsPoints = models.IntegerField()

    class Meta:
        db_table = 'credit_cards'

    def __str__(self):
        return f"Credit Card {self.CardID} - {self.CardType} - Balance: {self.CurrentBalance}"




class Feedback(models.Model):
    FeedbackID = models.AutoField(primary_key=True)
    CustomerID = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='feedbacks', blank=True, null=True)
    FeedbackDate = models.DateTimeField(auto_now_add=True)
    FeedbackType = models.CharField(max_length=50)
    ResolutionStatus = models.CharField(max_length=50)
    ResolutionDate = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'feedbacks'
        #ordering = ['-SubmissionDate']

    def __str__(self):
        return f"Feedback {self.FeedbackID} - Rating: {self.Rating}"




