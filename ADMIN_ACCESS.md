# 🔑 ADMIN ACCESS GUIDE

## 🚀 **AUTOMATIC ADMIN ACCOUNT**

When you run `setup.bat`, an admin account is **automatically created**!

### 📋 **Default Admin Credentials:**
```
Email: admin@admin.com
Password: admin123
```

## 🎯 **How to Access Admin Dashboard:**

### **Step 1: Start the System**
```bash
# Run this command:
setup.bat
```

### **Step 2: Look for Admin Account Message**
You'll see this in the backend terminal:
```
🔑 DEFAULT ADMIN ACCOUNT CREATED:
📧 Email: admin@admin.com
🔒 Password: admin
🌐 Login at: http://localhost:3000
👨💼 Admin Dashboard will be visible after login
```

### **Step 3: Login as Admin**
1. Go to http://localhost:3000
2. Click "Login"
3. Enter credentials:
   - **Email**: `admin@admin.com`
   - **Password**: `admin`
4. Click "Login"

### **Step 4: Access Admin Dashboard**
After login, you'll see **"Admin Dashboard"** in the navigation bar.
Click it to access all admin features!

## 📊 **Admin Dashboard Features:**

### **Overview Tab:**
- Total cases, active cases, found cases
- Total sightings, matches, pending verifications

### **Cases Tab:**
- View all missing person cases
- Mark persons as found
- View location history

### **Matches Tab:**
- See all AI face matches
- Verify or reject matches
- View confidence scores

### **Locations Tab:**
- Interactive map of all sightings
- Timeline of person movements
- GPS coordinates and timestamps

## 🔧 **Change Admin Password:**

1. Login as admin
2. Go to backend terminal
3. Run this command:
```bash
# In backend directory
cd backend
call venv\Scripts\activate
python -c "
from app.models.database import SessionLocal
from app.models.models import User
from app.utils.auth import get_password_hash
db = SessionLocal()
admin = db.query(User).filter(User.email == 'admin@admin.com').first()
admin.hashed_password = get_password_hash('your-new-password')
db.commit()
print('Admin password updated!')
db.close()
"
```

## 🆘 **Troubleshooting:**

### **Admin Dashboard not visible?**
- Make sure you're logged in as `admin@admin.com`
- Check if backend shows admin account creation message
- Try logging out and logging back in

### **Can't login as admin?**
- Verify credentials: `admin@admin.com` / `admin123`
- Check if backend is running on port 8000
- Look for error messages in backend terminal

### **Create additional admin users:**
1. Register normally at http://localhost:3000
2. Update database:
```sql
-- Open: backend/missing_persons.db
UPDATE users SET is_admin = 1 WHERE email = 'new-admin@email.com';
```

## ✅ **Quick Test:**
1. Run `setup.bat`
2. Go to http://localhost:3000
3. Login with `admin@admin.com` / `admin123`
4. See "Admin Dashboard" in navigation
5. Click it and explore all features!

**You're now ready to manage the Missing Person Detection System! 👨💼**