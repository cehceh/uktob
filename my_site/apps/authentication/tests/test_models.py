from django.test import TestCase
from ..models import CustomUser
# Create your tests here.


class CustomUserTestcase(TestCase):
    
    def test_string_method(self):
        obj = CustomUser.objects.create(
            username='root',
            password="@1234567",
            
        )
        user = CustomUser.objects.get(id=obj.id)
        expected_string = f"{user.username}"
        self.assertEqual(str(user.username), expected_string)

