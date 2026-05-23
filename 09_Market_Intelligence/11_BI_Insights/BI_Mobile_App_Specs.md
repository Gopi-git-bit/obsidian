# Mobile App Specifications: React Native

> **Cross-Platform Mobile Apps for Drivers and Customers**

---

## 1. Executive Summary

| Aspect | Specification |
|--------|---------------|
| **Framework** | React Native 0.73+ (Expo SDK 50+) |
| **Platforms** | iOS 14+ / Android 8.0+ |
| **Language** | TypeScript 5.0+ |
| **Navigation** | React Navigation 6.x |
| **State Management** | Zustand + TanStack Query |
| **Maps** | React Native Maps + Google Maps SDK |
| **Push Notifications** | Firebase Cloud Messaging (FCM) |
| **Storage** | AsyncStorage + MMKV |

---

## 2. Architecture Overview

### 2.1 Monorepo Structure (Recommended)

```
zippy-mobile/
├── apps/
│   ├── driver-app/          # Driver-specific app
│   │   ├── src/
│   │   ├── app.json
│   │   └── package.json
│   └── customer-app/        # Customer-specific app
│       ├── src/
│       ├── app.json
│       └── package.json
├── packages/
│   ├── shared-ui/           # Common UI components
│   ├── shared-api/          # API client + types
│   ├── shared-store/        # Shared state logic
│   └── shared-utils/        # Helper functions
├── package.json            # Root workspace
└── turbo.json             # Turborepo config
```

### 2.2 Tech Stack Details

```json
// package.json dependencies
{
  "dependencies": {
    "expo": "~50.0.0",
    "react": "18.2.0",
    "react-native": "0.73.6",
    "react-navigation": "^6.1.9",
    "@react-navigation/native-stack": "^6.9.17",
    "@react-navigation/bottom-tabs": "^6.5.11",
    "@tanstack/react-query": "^5.17.0",
    "zustand": "^4.5.0",
    "react-native-maps": "1.10.0",
    "@react-native-community/geolocation": "^3.1.0",
    "react-native-background-geolocation": "^4.14.0",
    "@react-native-firebase/app": "^18.7.0",
    "@react-native-firebase/messaging": "^18.7.0",
    "react-native-reanimated": "^3.6.0",
    "react-native-gesture-handler": "^2.14.0",
    "react-native-svg": "^14.1.0",
    "@gorhom/bottom-sheet": "^4.6.0",
    "react-native-vision-camera": "^3.8.0",
    "lottie-react-native": "^6.5.0",
    "react-native-haptic-feedback": "^2.2.0"
  }
}
```

---

## 3. Driver App Specifications

### 3.1 Core Features

| Feature | Priority | Description |
|---------|----------|-------------|
| **Job Matching** | P0 | Real-time job requests with accept/decline |
| **Navigation** | P0 | Turn-by-turn to pickup/delivery |
| **Earnings** | P0 | Daily/weekly earnings tracking |
| **Status Updates** | P0 | Update shipment status (5 stages) |
| **Document Upload** | P1 | Upload POD, vehicle docs |
| **Offline Mode** | P1 | Basic functionality without network |
| **Route Optimization** | P2 | Multi-stop route planning |
| **Fuel Tracker** | P2 | Log fuel expenses |

### 3.2 Screen Flow

```
Splash Screen
    ↓
Onboarding (First-time only)
    ↓
Login / Register
    ↓
Document Verification (KYC)
    ├─ Driving License
    ├─ Vehicle Registration
    ├─ Insurance Certificate
    └─ Bank Account Details
    ↓
Dashboard (Main Screen)
    ├─ Availability Toggle (ONLINE/OFFLINE)
    ├─ Today's Earnings
    └─ Job Request Cards (if available)
    ↓
Job Request Card (Push Notification)
    ├─ Accept (5-min timer)
    └─ Decline
    ↓
Active Job Screen
    ├─ Pickup Details
    ├─ Navigation Button
    ├─ Status Updates
    ├─ Contact Customer
    └─ Upload POD
    ↓
Earnings Screen
    └─ Daily/Weekly/Monthly breakdown
    ↓
Profile & Settings
    ├─ Personal Info
    ├─ Vehicle Details
    ├─ Bank Accounts
    ├─ Support
    └─ Logout
```

### 3.3 Key Screen Specifications

#### 3.3.1 Dashboard (Home)

```typescript
// DriverDashboard.tsx
interface DashboardData {
  isOnline: boolean;
  todayEarnings: number;
  weeklyEarnings: number;
  rating: number;
  completionRate: number;
  activeJob: ActiveJob | null;
  pendingRequest: JobRequest | null;
}

// UI Layout
┌─────────────────────────────────────┐
│  ☰  Driver Mode              🔔  💬  │
├─────────────────────────────────────┤
│                                     │
│     ┌─────────────────────────┐     │
│     │   🔴  GO OFFLINE        │     │
│     │   You're online and     │     │
│     │   ready for jobs        │     │
│     └─────────────────────────┘     │
│                                     │
│  ┌─────────────────────────────────┐│
│  │ 📊 TODAY'S EARNINGS           ││
│  │                                 ││
│  │         ₹1,247                ││
│  │     2 trips completed         ││
│  └─────────────────────────────────┘│
│                                     │
│  ┌─────────────────────────────────┐│
│  │ ⭐ Your Rating      4.8/5       ││
│  │ 📈 Completion Rate  96%        ││
│  └─────────────────────────────────┘│
│                                     │
│  ┌─────────────────────────────────┐│
│  │ 🚛 ACTIVE JOB (if any)         ││
│  │                                 ││
│  │   Chennai → Coimbatore         ││
│  │   506 km remaining             ││
│  │   ETA: 6:30 PM                 ││
│  │                                 ││
│  │   [NAVIGATE]  [UPDATE STATUS]  ││
│  └─────────────────────────────────┘│
│                                     │
│  ┌─────────────────────────────────┐│
│  │ 💰 QUICK STATS                 ││
│  │ This Week: ₹8,450              ││
│  │ This Month: ₹34,200            ││
│  └─────────────────────────────────┘│
│                                     │
├─────────────────────────────────────┤
│  🏠      💼       💰       👤      │
│ Home    Jobs   Earnings  Profile   │
└─────────────────────────────────────┘
```

**Key Behaviors:**
- **Online Toggle:** Large button at top. When offline, shows "GO ONLINE" in green.
- **Job Notifications:** Full-screen modal appears over any screen when job request arrives.
- **Background Location:** Must track when app is backgrounded (for customer tracking).

#### 3.3.2 Job Request Modal

```typescript
interface JobRequest {
  id: string;
  pickup: {
    address: string;
    lat: number;
    lng: number;
    distance: number; // from current location
  };
  delivery: {
    address: string;
    lat: number;
    lng: number;
  };
  materialType: string;
  weight: number;
  vehicleRequired: string;
  offeredPrice: number;
  expiresAt: Date; // 5 minutes from now
}
```

```
┌─────────────────────────────────────┐
│         [5:23 remaining]            │
│                                     │
│  📦 NEW JOB REQUEST                 │
│                                     │
│  ┌─────────────────────────────────┐│
│  │ FROM                            ││
│  │ 📍 Anna Nagar, Chennai         ││
│  │   2.3 km away                  ││
│  │                                 ││
│  │ TO                              ││
│  │ 📍 Gandhipuram, Coimbatore     ││
│  │                                 ││
│  │ Material: Electronics          ││
│  │ Weight: 500 kg                 ││
│  │ Vehicle: Pickup (Open)         ││
│  └─────────────────────────────────┘│
│                                     │
│         💰 ₹8,500                   │
│         Your earnings               │
│                                     │
│  ┌─────────────────────────────────┐│
│  │                                 ││
│  │        ✅ ACCEPT                ││
│  │                                 ││
│  └─────────────────────────────────┘│
│                                     │
│           ❌ DECLINE                │
│                                     │
└─────────────────────────────────────┘
```

**Animation:**
- Slide up from bottom with bounce
- Timer counts down (5 minutes)
- Haptic feedback on accept/decline
- Auto-dismiss on expiry with decline action

#### 3.3.3 Active Job Screen

```typescript
interface ActiveJob {
  bookingId: string;
  pickup: Location;
  delivery: Location;
  customer: {
    name: string;
    phone: string;
  };
  material: {
    type: string;
    weight: number;
    description: string;
  };
  price: number;
  currentStatus: JobStatus;
  timeline: TimelineEvent[];
}

type JobStatus = 
  | 'en_route_pickup'
  | 'at_pickup'
  | 'loading'
  | 'in_transit'
  | 'at_delivery'
  | 'unloading'
  | 'completed';
```

**Status Update Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│  ← Active Job                                    📞  💬  🗺️  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TIMELINE                                                   │
│  ●───────○───────○───────○───────○────────○───────○         │
│  EN      AT      LOAD   ON     AT      UNLOAD   DONE        │
│  ROUTE  PICKUP          WAY   DELIVERY                       │
│  PICKUP                                                     │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 📍 PICKUP                                             ││
│  │ Anna Nagar, Chennai 600040                           ││
│  │ Contact: Rajesh Kumar (9876543210)                   ││
│  │                                                       ││
│  │ [📍 NAVIGATE]  [📞 CALL]  [💬 MESSAGE]              ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 📦 SHIPMENT DETAILS                                    ││
│  │ Electronics - 500 kg                                   ││
│  │ Handle with care - Fragile items                       ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 📍 DELIVERY                                           ││
│  │ Gandhipuram, Coimbatore 641012                        ││
│  │ Contact: Suresh (9876543211)                           ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                                                         ││
│  │          ✅ MARK AS ARRIVED AT PICKUP                 ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│     [UPLOAD PHOTOS]        [REPORT ISSUE]                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Status Button States:**

| Current Status | Button Text | Next Status |
|----------------|-------------|-------------|
| en_route_pickup | "ARRIVED AT PICKUP" | at_pickup |
| at_pickup | "START LOADING" | loading |
| loading | "LOADING COMPLETE" | in_transit |
| in_transit | "ARRIVED AT DELIVERY" | at_delivery |
| at_delivery | "START UNLOADING" | unloading |
| unloading | "DELIVERY COMPLETE" | completed |
| completed | "UPLOAD POD" | - |

Each status update requires:
- GPS location verification (within 100m of target)
- Timestamp
- Optional photo evidence

#### 3.3.4 Earnings Screen

```typescript
interface EarningsData {
  today: {
    total: number;
    trips: number;
    incentives: number;
  };
  thisWeek: {
    total: number;
    dailyBreakdown: DailyEarning[];
  };
  thisMonth: {
    total: number;
    weekBreakdown: WeekEarning[];
  };
  allTime: {
    total: number;
    totalTrips: number;
    averagePerTrip: number;
  };
}
```

```
┌─────────────────────────────────────────────────────────────┐
│  ← Earnings                                     💰          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  TODAY                                                   ││
│  │                                                         ││
│  │              ₹1,247                                    ││
│  │      2 trips completed                                  ││
│  │                                                         ││
│  │  ┌─────────────────────────────────────────────────┐   ││
│  │  │ Trip #1: Chennai→Ambattur      ₹650            │   ││
│  │  │ Trip #2: Guindy→Sriperumbudur  ₹597            │   ││
│  │  └─────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  [TODAY] [THIS WEEK] [THIS MONTH] [ALL TIME]               │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                                                         ││
│  │  📊 THIS WEEK                                           ││
│  │                                                         ││
│  │  Mon ▓▓▓▓▓▓▓▓░░ ₹850                                   ││
│  │  Tue ▓▓▓▓▓▓▓▓▓▓ ₹1,200                                 ││
│  │  Wed ▓▓▓▓▓▓▓▓▓▓ ₹1,450                                 ││
│  │  Thu ▓▓▓▓▓▓▓▓▓▓ ₹1,100                                 ││
│  │  Fri ▓▓▓▓▓▓▓▓▓▓ ₹1,380                                 ││
│  │  Sat ▓▓▓▓▓▓▓▓▓▓ ₹1,700                                 ││
│  │  Sun ▓▓▓▓░░░░░░ ₹800 (so far)                          ││
│  │                                                         ││
│  │         Total: ₹8,480                                   ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│     [VIEW TRIP HISTORY]    [DOWNLOAD STATEMENT]            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Customer App Specifications

### 4.1 Core Features

| Feature | Priority | Description |
|---------|----------|-------------|
| **Post Requirement** | P0 | Create new booking with AI pricing |
| **Live Tracking** | P0 | Real-time shipment tracking |
| **Booking History** | P0 | View past and active bookings |
| **Price Estimator** | P0 | Get instant price quotes |
| **Payment** | P0 | In-app payments (Razorpay) |
| **Rating & Review** | P1 | Rate drivers after delivery |
| **Address Book** | P1 | Save frequently used addresses |
| **Notifications** | P1 | Booking updates via push |
| **Support Chat** | P2 | In-app customer support |

### 4.2 Screen Flow

```
Splash Screen
    ↓
Onboarding (3 slides)
    ├─ Slide 1: Fast booking
    ├─ Slide 2: Live tracking
    └─ Slide 3: Best prices
    ↓
Login / Register
    ├─ Phone number + OTP
    └─ Google/Apple Sign-in
    ↓
Home Dashboard
    ├─ Post New Requirement (CTA)
    ├─ Active Shipments
    ├─ Recent Bookings
    └─ Price Trend
    ↓
New Booking Flow
    ├─ Step 1: Pickup Location
    ├─ Step 2: Delivery Location
    ├─ Step 3: Shipment Details
    ├─ Step 4: Vehicle Selection
    └─ Step 5: Price & Payment
    ↓
Tracking Screen
    ├─ Live map with vehicle
    ├─ Driver info & contact
    ├─ ETA countdown
    └─ Delivery timeline
    ↓
Booking Details
    ├─ Full itinerary
    ├─ Invoice
    ├─ Download POD
    └─ Rate Driver
    ↓
Profile
    ├─ Personal info
    ├─ Saved addresses
    ├─ Payment methods
    ├─ Support
    └─ Settings
```

### 4.3 Key Screen Specifications

#### 4.3.1 Customer Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│  ☰  Good Morning, Rajesh!                    🔔  💬  👤  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                                                         ││
│  │     📦 Post a New Requirement                           ││
│  │                                                         ││
│  │  Need to move something? Get instant quotes!          ││
│  │                                                         ││
│  │     [GET STARTED →]                                    ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  📍 ACTIVE SHIPMENTS (2)                                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 🚚 Chennai → Coimbatore                                ││
│  │ In Transit • ETA: 4:30 PM                              ││
│  │ Driver: Kumar M. ⭐ 4.9                                  ││
│  │ [TRACK →]                                              ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 🚚 Guindy → Sriperumbudur                              ││
│  │ Driver Assigned • Pickup at 2:00 PM                  ││
│  │ Driver: Arun K. ⭐ 4.7                                  ││
│  │ [VIEW DETAILS →]                                       ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  📊 MARKET INSIGHTS                                         │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                                                         ││
│  │   Price Trend (Chennai→Coimbatore)                     ││
│  │   ▁▂▄▆██▇▃▁▂▄▆ (last 7 days)                           ││
│  │                                                         ││
│  │   Current: ₹18,400  (Great time to book!)              ││
│  │   Average: ₹21,500                                     ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
├─────────────────────────────────────┬───────────────────────┤
│  🏠 HOME                           │ 💼 BOOKINGS            │
│  💳 PAYMENTS                       │ 👤 PROFILE             │
└─────────────────────────────────────┴───────────────────────┘
```

#### 4.3.2 New Booking - Step 1: Locations

```
┌─────────────────────────────────────────────────────────────┐
│  ← New Booking                        1 of 5  [Cancel]      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📍 PICKUP LOCATION                                         │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 📍 Search pickup location...                           ││
│  │                                                       ││
│  │ [Use Current Location]                               ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  📍 DELIVERY LOCATION                                       │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 📍 Search delivery location...                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                                                         ││
│  │   ┌─────────────────────────────────────────────┐     ││
│  │   │                                             │     ││
│  │   │              [MAP PREVIEW]                  │     ││
│  │   │                                             │     ││
│  │   │         Chennai → Coimbatore                │     ││
│  │   │              506 km                         │     ││
│  │   │                                             │     ││
│  │   └─────────────────────────────────────────────┘     ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                                                         ││
│  │                    [CONTINUE →]                         ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 4.3.3 New Booking - Step 3: Shipment Details

```
┌─────────────────────────────────────────────────────────────┐
│  ← Shipment Details                  3 of 5  [Cancel]       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📦 WHAT ARE YOU SHIPPING?                                  │
│                                                             │
│  Material Type*                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ ▼ Select material type...                              ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  Options: Electronics | Furniture | Textiles | Machinery    │
│            | Raw Materials | Packaged Goods | Other          │
│                                                             │
│  WEIGHT (kg)*                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━  [ 500 ] kg                 ││
│  └─────────────────────────────────────────────────────────┘│
│  Slider: 50kg ———————●—————— 40,000kg                      │
│                                                             │
│  SHIPMENT VALUE (for insurance)                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ ₹ [50,000]                                             ││
│  └─────────────────────────────────────────────────────────┘│
│  Insurance coverage: ₹50,000 (₹500 - 1% of value)          │
│                                                             │
│  SPECIAL HANDLING                                         │
│  ☑️ Fragile Items                                           │
│  ☐ Oversized Load                                           │
│  ☐ Temperature Controlled                                   │
│  ☐ Hazardous Materials                                      │
│                                                             │
│  ADD PHOTOS (Optional, max 5)                              │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                       │
│  │ +  │ │    │ │    │ │    │ │    │                       │
│  └────┘ └────┘ └────┘ └────┘ └────┘                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                                                         ││
│  │                    [CONTINUE →]                         ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 4.3.4 New Booking - Step 5: Price & Payment

```
┌─────────────────────────────────────────────────────────────┐
│  ← Price & Payment                    5 of 5  [Cancel]      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  💰 PRICE ESTIMATE                                          │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                                                         ││
│  │              ₹18,408                                   ││
│  │           Total Amount                                  ││
│  │                                                         ││
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ││
│  │                                                         ││
│  │  Base Cost                          ₹12,500            ││
│  │  Festival Surcharge (+20%)          +₹2,500            ││
│  │  Platform Fee (4%)                   +₹600             ││
│  │  GST (18%)                         +₹2,808             ││
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ││
│  │  TOTAL                             ₹18,408             ││
│  │                                                         ││
│  │  vs Market Rate: ₹22,000                              ││
│  │  🎉 You save ₹3,592 (16%)!                              ││
│  │                                                         ││
│  │  [⏱️ Lock price for 30 min]                            ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  💳 PAYMENT METHOD                                          │
│                                                             │
│  ● UPI                                                      │
│    Google Pay, PhonePe, Paytm                              │
│                                                             │
│  ○ Credit/Debit Card                                        │
│    Visa, Mastercard, RuPay                                 │
│                                                             │
│  ○ Net Banking                                              │
│                                                             │
│  ○ Pay on Delivery                                          │
│    ₹500 additional handling fee                            │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                                                         ││
│  │            [CONFIRM & PAY ₹18,408]                      ││
│  │                                                         ││
│  │  By confirming, you agree to our Terms & Conditions    ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 4.3.5 Live Tracking Screen

```
┌─────────────────────────────────────────────────────────────┐
│  ← Tracking                          #ZI123456               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                                                         ││
│  │              [FULL SCREEN MAP]                        ││
│  │                                                         ││
│  │      🚚 ← Truck icon moving on route                  ││
│  │                                                         ││
│  │         Chennai —————————→ Coimbatore                ││
│  │                                                         ││
│  │         206 km remaining                              ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  ⏱️ ARRIVING IN 4h 30m                                 ││
│  │  Expected by 6:30 PM                                    ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  🚛 DRIVER                                              ││
│  │                                                         ││
│  │  ┌───┐  Kumar M.                          ⭐ 4.9        ││
│  │  │ 👤│  TN 01 AB 1234                                  ││
│  │  └───┘                                                 ││
│  │  [📞 CALL]  [💬 MESSAGE]                               ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  📍 DELIVERY DETAILS                                        │
│  Gandhipuram, Coimbatore 641012                            │
│  Contact: Suresh - 9876543211                              │
│                                                             │
│  📋 TIMELINE                                                │
│  ● 10:30 AM  Booking Confirmed                             │
│  ● 10:45 AM  Driver Assigned                               │
│  ● 11:30 AM  Pickup Complete                                 │
│  ○ ────────  In Transit (Current)                          │
│  ○           Delivery Pending                               │
│                                                             │
│  [SHARE TRACKING LINK]                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Shared Components Library

### 5.1 Core UI Components

```typescript
// packages/shared-ui/src/components/Button.tsx
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger' | 'ghost';
  size: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  onPress: () => void;
  children: React.ReactNode;
}

// Style specifications
const buttonStyles = {
  primary: {
    backgroundColor: '#2563eb',
    color: '#ffffff',
    pressed: '#1d4ed8',
  },
  secondary: {
    backgroundColor: '#e5e7eb',
    color: '#374151',
    pressed: '#d1d5db',
  },
  sizes: {
    sm: { padding: 8, fontSize: 14, minHeight: 36 },
    md: { padding: 12, fontSize: 16, minHeight: 44 },
    lg: { padding: 16, fontSize: 18, minHeight: 56 },
  },
};
```

### 5.2 Map Components

```typescript
// packages/shared-ui/src/components/MapView.tsx
interface MapViewProps {
  region: Region;
  markers: MapMarker[];
  route?: Polyline;
  showsUserLocation?: boolean;
  followsUserLocation?: boolean;
  onMarkerPress?: (marker: MapMarker) => void;
  onRegionChange?: (region: Region) => void;
}

// Native module for background location
interface BackgroundLocationConfig {
  desiredAccuracy: 'high' | 'medium' | 'low';
  distanceFilter: number; // meters
  stopOnTerminate: boolean;
  startOnBoot: boolean;
  notificationTitle?: string;
  notificationText?: string;
}
```

---

## 6. Push Notification System

### 6.1 FCM Integration

```typescript
// Driver App Notifications
const DRIVER_NOTIFICATIONS = {
  // High priority - requires immediate action
  JOB_REQUEST: {
    title: '📦 New Job Available!',
    body: '₹8,500 • Chennai → Coimbatore',
    priority: 'high',
    sound: 'job_alert.mp3',
    vibrate: [0, 500, 200, 500],
    data: {
      type: 'JOB_REQUEST',
      jobId: string,
      expiresAt: string,
    },
    actions: ['ACCEPT', 'DECLINE'],
  },
  
  // Payment notifications
  PAYMENT_RECEIVED: {
    title: '💰 Payment Received',
    body: '₹{amount} credited to your wallet',
    priority: 'normal',
  },
  
  // Status updates
  RATING_RECEIVED: {
    title: '⭐ New Rating',
    body: 'You received a 5-star rating!',
    priority: 'low',
  },
};

// Customer App Notifications
const CUSTOMER_NOTIFICATIONS = {
  DRIVER_ASSIGNED: {
    title: '🚛 Driver Assigned',
    body: '{driverName} is on the way to pickup',
    priority: 'high',
  },
  
  PICKUP_COMPLETE: {
    title: '✅ Pickup Complete',
    body: 'Your shipment is now in transit',
    priority: 'normal',
  },
  
  DELIVERY_COMPLETE: {
    title: '🎉 Delivery Complete',
    body: 'Your shipment has been delivered',
    priority: 'high',
    actions: ['RATE_DRIVER'],
  },
  
  DELAY_ALERT: {
    title: '⚠️ Delay Alert',
    body: 'Your shipment is delayed by {delay} minutes',
    priority: 'high',
  },
};
```

### 6.2 Notification Handler

```typescript
// lib/notifications.ts
import messaging from '@react-native-firebase/messaging';

export async function setupNotifications() {
  // Request permission
  const authStatus = await messaging().requestPermission();
  const enabled =
    authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
    authStatus === messaging.AuthorizationStatus.PROVISIONAL;
  
  if (enabled) {
    // Get FCM token
    const token = await messaging().getToken();
    await registerDeviceToken(token);
    
    // Listen for token refresh
    messaging().onTokenRefresh(registerDeviceToken);
    
    // Handle foreground messages
    messaging().onMessage(handleForegroundMessage);
    
    // Handle background/quit state
    messaging().setBackgroundMessageHandler(handleBackgroundMessage);
  }
}

async function handleForegroundMessage(message: RemoteMessage) {
  const { type, ...data } = message.data || {};
  
  switch (type) {
    case 'JOB_REQUEST':
      showJobRequestModal(data);
      break;
    case 'DRIVER_ASSIGNED':
      showInAppNotification(message);
      break;
    // ... other cases
  }
}
```

---

## 7. Background Location Tracking

### 7.1 Driver Location Tracking

```typescript
// services/locationTracking.ts
import BackgroundGeolocation from 'react-native-background-geolocation';

export async function startLocationTracking(bookingId: string) {
  await BackgroundGeolocation.ready({
    // Geolocation Config
    desiredAccuracy: BackgroundGeolocation.DESIRED_ACCURACY_HIGH,
    distanceFilter: 50, // Update every 50 meters
    stopTimeout: 5, // Stop after 5 minutes stationary
    
    // Android notification
    notification: {
      title: 'Location tracking active',
      text: 'Sharing location for booking #{bookingId}',
      channelName: 'Location Tracking',
    },
    
    // HTTP config
    url: `${API_URL}/api/v1/tracking/location`,
    headers: {
      Authorization: `Bearer ${getAuthToken()}`,
    },
    params: {
      bookingId,
    },
    
    // iOS permissions
    locationAuthorizationRequest: 'Always',
    
    // Activity type
    activityType: BackgroundGeolocation.ACTIVITY_TYPE_AUTOMOTIVE_NAVIGATION,
  });
  
  await BackgroundGeolocation.start();
}

export async function stopLocationTracking() {
  await BackgroundGeolocation.stop();
}

// Listen to location updates
BackgroundGeolocation.onLocation((location) => {
  // Location sent automatically via HTTP
  console.log('Location update:', location);
});
```

---

## 8. Offline Support

### 8.1 Queue for Offline Actions

```typescript
// stores/offlineQueue.ts
interface QueuedAction {
  id: string;
  type: 'STATUS_UPDATE' | 'POD_UPLOAD' | 'LOCATION_UPDATE';
  payload: any;
  timestamp: number;
  retryCount: number;
}

export const useOfflineQueue = create<OfflineQueueState>((set, get) => ({
  queue: [],
  
  addToQueue: (action: Omit<QueuedAction, 'id' | 'timestamp' | 'retryCount'>) => {
    const newAction: QueuedAction = {
      ...action,
      id: generateUUID(),
      timestamp: Date.now(),
      retryCount: 0,
    };
    set((state) => ({ queue: [...state.queue, newAction] }));
  },
  
  processQueue: async () => {
    const { queue } = get();
    const netInfo = await NetInfo.fetch();
    
    if (!netInfo.isConnected || queue.length === 0) return;
    
    for (const action of queue) {
      try {
        await processAction(action);
        set((state) => ({
          queue: state.queue.filter((a) => a.id !== action.id),
        }));
      } catch (error) {
        // Retry with exponential backoff
        if (action.retryCount < 3) {
          set((state) => ({
            queue: state.queue.map((a) =>
              a.id === action.id
                ? { ...a, retryCount: a.retryCount + 1 }
                : a
            ),
          }));
        }
      }
    }
  },
}));
```

---

## 9. Security Implementation

### 9.1 Certificate Pinning

```typescript
// ssl-pinning configuration
const PINNED_CERTIFICATES = {
  'api.zippylogitech.in': [
    'sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=', // Primary
    'sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=', // Backup
  ],
};
```

### 9.2 Biometric Authentication (Optional)

```typescript
// For sensitive actions like viewing earnings
import ReactNativeBiometrics from 'react-native-biometrics';

export async function requireBiometricAuth(): Promise<boolean> {
  const { available, biometryType } = await ReactNativeBiometrics.isSensorAvailable();
  
  if (!available) return true; // Skip if not available
  
  const { success } = await ReactNativeBiometrics.simplePrompt({
    promptMessage: 'Confirm your identity',
  });
  
  return success;
}
```

---

## 10. Testing Strategy

### 10.1 Test Structure

```
__tests__/
├── unit/
│   ├── components/
│   ├── hooks/
│   └── utils/
├── integration/
│   ├── booking-flow.test.tsx
│   └── driver-job-flow.test.tsx
└── e2e/
    ├── customer-journey.test.ts
    └── driver-journey.test.ts (Detox)
```

### 10.2 Detox E2E Example

```typescript
// e2e/driver-job-flow.test.ts
import { device, expect, element, by } from 'detox';

describe('Driver Job Flow', () => {
  beforeAll(async () => {
    await device.launchApp();
  });
  
  it('should login as driver', async () => {
    await element(by.id('phone-input')).typeText('9876543210');
    await element(by.id('login-button')).tap();
    await element(by.id('otp-input')).typeText('123456');
    await expect(element(by.id('driver-dashboard'))).toBeVisible();
  });
  
  it('should go online and receive job request', async () => {
    await element(by.id('online-toggle')).tap();
    await expect(element(by.id('job-request-modal'))).toBeVisible();
  });
  
  it('should accept job request', async () => {
    await element(by.id('accept-job-button')).tap();
    await expect(element(by.id('active-job-screen'))).toBeVisible();
  });
  
  it('should complete all status updates', async () => {
    // Arrived at pickup
    await element(by.id('status-update-button')).tap();
    await expect(element(by.text('Loading'))).toBeVisible();
    
    // Loading complete
    await element(by.id('status-update-button')).tap();
    await expect(element(by.text('In Transit'))).toBeVisible();
  });
});
```

---

## 11. Build & Deployment

### 11.1 Environment Configuration

```bash
# .env.development
API_URL=https://api-staging.zippylogitech.in
WS_URL=wss://api-staging.zippylogitech.in
MAPBOX_TOKEN=pk.test...
SENTRY_DSN=https://...

# .env.production
API_URL=https://api.zippylogitech.in
WS_URL=wss://api.zippylogitech.in
MAPBOX_TOKEN=pk.prod...
SENTRY_DSN=https://...
```

### 11.2 Build Commands

```bash
# iOS
cd apps/driver-app
npx expo prebuild --platform ios
cd ios
fastlane beta  # TestFlight
fastlane release  # App Store

# Android
cd apps/driver-app
npx expo prebuild --platform android
cd android
fastlane beta  # Internal Testing
fastlane release  # Play Store
```

### 11.3 OTA Updates (Expo Updates)

```typescript
// Automatic OTA updates on app start
import * as Updates from 'expo-updates';

async function checkForUpdates() {
  try {
    const update = await Updates.checkForUpdateAsync();
    if (update.isAvailable) {
      await Updates.fetchUpdateAsync();
      await Updates.reloadAsync();
    }
  } catch (error) {
    console.log('Update check failed:', error);
  }
}
```

---

## 12. Performance Optimization

### 12.1 Bundle Size Management

```typescript
// Use Hermes engine (enabled by default in Expo 50+)
// Enable ProGuard for Android
// Use inline requires for heavy modules

// Lazy load heavy components
const HeavyMap = React.lazy(() => import('./components/HeavyMap'));

// Preload critical images
import { Image } from 'react-native';

Image.prefetch([
  require('./assets/truck-marker.png'),
  require('./assets/driver-avatar.png'),
]);
```

### 12.2 List Optimization

```typescript
// Use FlashList instead of FlatList for better performance
import { FlashList } from '@shopify/flash-list';

<FlashList
  data={earnings}
  renderItem={renderEarningItem}
  estimatedItemSize={80}
  keyExtractor={(item) => item.id}
/>
```

---

## 13. Development Timeline

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| **Week 1** | 5 days | Project setup, navigation, auth, base components |
| **Week 2** | 5 days | Driver dashboard, job matching, availability toggle |
| **Week 3** | 5 days | Active job flow, status updates, navigation integration |
| **Week 4** | 5 days | Customer app screens, booking flow, price display |
| **Week 5** | 5 days | Live tracking, maps, timeline |
| **Week 6** | 5 days | Push notifications, offline support, polish |
| **Week 7** | 5 days | Testing (unit, integration, e2e), bug fixes |
| **Week 8** | 5 days | Build optimization, store submission prep |

**Total: 8 weeks for both apps**

---

## 14. Integration Matrix

| Backend Service | Driver App | Customer App | Notes |
|-----------------|------------|--------------|-------|
| REST API | ✅ All endpoints | ✅ All endpoints | Axios |
| WebSocket | ✅ Job notifications, tracking updates | ✅ Tracking updates | Socket.io |
| Push Notifications | ✅ FCM | ✅ FCM | Firebase |
| Background Location | ✅ Continuous tracking | ❌ Not needed | BackgroundGeolocation |
| Maps | ✅ Route navigation | ✅ Tracking view | React Native Maps |
| Razorpay | ❌ Not needed | ✅ Payments | Native SDK |
| Camera | ✅ POD upload | ❌ Not needed | react-native-vision-camera |
| File Storage | ✅ Document upload | ❌ Minimal | AWS S3 pre-signed URLs |

---

*Document Version: 1.0*
*Last Updated: April 2026*
*Total Specifications: ~800 lines*
