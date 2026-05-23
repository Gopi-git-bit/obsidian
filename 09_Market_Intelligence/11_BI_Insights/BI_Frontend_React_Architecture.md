# Frontend Architecture: React 18 + TypeScript

> **Complete UI/UX Specification for Zippy Logitech Logistics Platform**

---

## 1. Executive Summary

| Aspect | Specification |
|--------|---------------|
| **Framework** | React 18.2+ with TypeScript 5.0+ |
| **Styling** | Tailwind CSS 3.4+ + Headless UI |
| **State Management** | Zustand (lightweight) + React Query (server state) |
| **Maps** | Mapbox GL JS / Google Maps JavaScript API |
| **Real-time** | Socket.io Client |
| **Charts** | Recharts / Tremor React |
| **Build Tool** | Vite 5.0+ |

---

## 2. Tech Stack Deep Dive

### 2.1 Core Dependencies

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.0",
    "@tanstack/react-query": "^5.17.0",
    "zustand": "^4.5.0",
    "axios": "^1.6.0",
    "socket.io-client": "^4.7.0",
    "date-fns": "^3.3.0",
    "react-hook-form": "^7.49.0",
    "zod": "^3.22.0",
    "@hookform/resolvers": "^3.3.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "@headlessui/react": "^1.7.0",
    "@heroicons/react": "^2.1.0",
    "@tremor/react": "^3.13.0"
  }
}
```

### 2.2 Tailwind Configuration

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Brand Colors - Logistics Industry
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb', // Main brand
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        // Status Colors
        status: {
          pending: '#f59e0b',    // Amber
          confirmed: '#3b82f6',  // Blue
          inTransit: '#8b5cf6',  // Purple
          delivered: '#10b981',  // Green
          cancelled: '#ef4444',  // Red
          delayed: '#f97316',    // Orange
        },
        // Freight Type Colors
        freight: {
          ftl: '#059669',     // Green - Full Truckload
          ptl: '#d97706',     // Amber - Part Truckload
          ltl: '#7c3aed',     // Violet - Less Truckload
          express: '#dc2626', // Red - Express
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

export default config
```

---

## 3. Project Structure

```
src/
├── api/                    # API layer
│   ├── client.ts          # Axios instance
│   ├── endpoints/         # API endpoint definitions
│   │   ├── auth.ts
│   │   ├── bookings.ts
│   │   ├── pricing.ts
│   │   ├── tracking.ts
│   │   └── fleet.ts
│   └── types/             # API response types
├── components/            # Reusable components
│   ├── ui/               # Base UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Select.tsx
│   │   ├── Card.tsx
│   │   ├── Modal.tsx
│   │   ├── Table.tsx
│   │   ├── Badge.tsx
│   │   └── Loading.tsx
│   ├── forms/            # Form-specific components
│   │   ├── AddressInput.tsx
│   │   ├── VehicleSelect.tsx
│   │   ├── MaterialTypeSelect.tsx
│   │   └── DateTimePicker.tsx
│   ├── maps/             # Map components
│   │   ├── LiveMap.tsx
│   │   ├── RoutePreview.tsx
│   │   ├── VehicleMarker.tsx
│   │   └── HeatmapLayer.tsx
│   └── charts/           # Chart components
│       ├── PriceTrendChart.tsx
│       ├── UtilizationChart.tsx
│       └── DemandHeatmap.tsx
├── hooks/                 # Custom React hooks
│   ├── useAuth.ts
│   ├── usePricing.ts
│   ├── useTracking.ts
│   ├── useSocket.ts
│   └── useGeolocation.ts
├── stores/               # Zustand state stores
│   ├── authStore.ts
│   ├── bookingStore.ts
│   ├── mapStore.ts
│   └── uiStore.ts
├── pages/                # Route pages
│   ├── public/
│   │   ├── Landing.tsx
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   └── PricingEstimator.tsx
│   ├── customer/
│   │   ├── Dashboard.tsx
│   │   ├── NewBooking.tsx
│   │   ├── BookingsList.tsx
│   │   ├── BookingDetail.tsx
│   │   ├── Tracking.tsx
│   │   └── Profile.tsx
│   ├── driver/
│   │   ├── DriverDashboard.tsx
│   │   ├── JobRequests.tsx
│   │   ├── ActiveJob.tsx
│   │   ├── Earnings.tsx
│   │   └── Documents.tsx
│   └── admin/
│       ├── AdminDashboard.tsx
│       ├── FleetManagement.tsx
│       ├── PricingControls.tsx
│       ├── DisputeResolution.tsx
│       └── Analytics.tsx
├── types/                # Global TypeScript types
│   ├── booking.ts
│   ├── user.ts
│   ├── vehicle.ts
│   └── pricing.ts
├── utils/                # Utility functions
│   ├── formatters.ts
│   ├── validators.ts
│   ├── constants.ts
│   └── helpers.ts
├── lib/                  # Third-party library configs
│   ├── queryClient.ts
│   └── socket.ts
└── App.tsx              # Main app component
```

---

## 4. Key Screens Specification

### 4.1 Customer Dashboard

**Route:** `/customer/dashboard`
**Purpose:** Central hub for shipment management

```typescript
// Page Structure
interface DashboardStats {
  activeBookings: number;
  completedThisMonth: number;
  totalSpent: number;
  savingsVsMarket: number;
}

interface RecentBooking {
  id: string;
  origin: string;
  destination: string;
  status: BookingStatus;
  vehicleType: string;
  price: number;
  eta: string;
  driver?: {
    name: string;
    phone: string;
    rating: number;
  };
}
```

**UI Components:**
1. **Stats Cards Row** (4 cards)
   - Active Shipments
   - Completed This Month
   - Total Spent
   - Savings vs Market Rate

2. **Quick Action Buttons**
   - "Post New Requirement" (Primary CTA)
   - "Track Shipment"
   - "View History"

3. **Live Shipments Section**
   - Map view with live vehicle positions
   - List view with ETA and driver info
   - Real-time status updates via Socket.io

4. **Price Trend Widget**
   - 7-day price trend chart
   - Current market rate indicator
   - AI-powered best booking time suggestion

**Responsive Breakpoints:**
- Mobile (<640px): Single column, stacked cards
- Tablet (640-1024px): 2-column grid
- Desktop (>1024px): 4-column stats + 2-column layout

---

### 4.2 New Booking Form

**Route:** `/customer/booking/new`
**Purpose:** Create new freight booking with AI price estimate

```typescript
interface BookingFormData {
  // Pickup Details
  pickup: {
    address: string;
    lat: number;
    lng: number;
    contactName: string;
    contactPhone: string;
    preferredDate: Date;
    preferredTime: 'morning' | 'afternoon' | 'evening' | 'flexible';
  };
  
  // Delivery Details
  delivery: {
    address: string;
    lat: number;
    lng: number;
    contactName: string;
    contactPhone: string;
  };
  
  // Shipment Details
  shipment: {
    materialType: string;
    weight: number; // in kg
    volume?: number; // in cbm
    value: number; // for insurance
    handlingRequirements: string[];
    photos?: File[];
  };
  
  // Vehicle Selection
  vehiclePreference: 'ftl' | 'ptl' | 'ltl' | 'any';
  vehicleType?: string;
  
  // Pricing
  quotedPrice: number;
  platformFee: number;
  gstAmount: number;
  totalAmount: number;
}
```

**Form Sections:**

1. **Route Selection (Step 1)**
   - Origin input with geocoding
   - Destination input with geocoding
   - Distance display (auto-calculated)
   - Map preview with route

2. **Shipment Details (Step 2)**
   - Material type dropdown (predefined list)
   - Weight input (kg)
   - Volume input (optional, cbm)
   - Value input (for insurance calculation)
   - Special handling checkboxes

3. **Vehicle Selection (Step 3)**
   - FTL/PTL/LTL toggle
   - Vehicle type recommendations based on weight/volume
   - Estimated space utilization %

4. **Pricing Review (Step 4)**
   - AI-generated price estimate
   - Breakdown: Base + Scenario surcharge + Platform fee + GST
   - Market rate comparison
   - "Lock Price for 30 minutes" button

5. **Confirmation (Step 5)**
   - Summary review
   - Terms & conditions
   - Payment method selection
   - Confirm booking

**Validation Rules:**
- Phone: 10 digits, Indian format
- Weight: 50kg - 40,000kg range
- Value: Min ₹1,000 for insurance
- Photos: Max 5, each <5MB

---

### 4.3 Live Tracking Page

**Route:** `/customer/tracking/:bookingId`
**Purpose:** Real-time shipment tracking

```typescript
interface TrackingData {
  bookingId: string;
  status: BookingStatus;
  vehicle: {
    type: string;
    number: string;
    capacity: number;
  };
  driver: {
    name: string;
    phone: string;
    rating: number;
    photo?: string;
  };
  route: {
    origin: GeoPoint;
    destination: GeoPoint;
    currentPosition: GeoPoint;
    waypoints: GeoPoint[];
    distanceRemaining: number;
    eta: Date;
  };
  timeline: TimelineEvent[];
}

interface TimelineEvent {
  timestamp: Date;
  status: string;
  location: string;
  description: string;
  icon: string;
}
```

**UI Features:**
1. **Full-screen Map**
   - Vehicle position (auto-updating every 30s)
   - Route polyline
   - Origin/destination markers
   - Traffic layer toggle

2. **Driver Info Card**
   - Photo, name, rating
   - Call button
   - Share location button

3. **ETA Display**
   - Large countdown timer
   - "Arrived at pickup" / "In transit" / "Delivered" status
   - Delay alerts if applicable

4. **Timeline Sidebar**
   - Vertical timeline of events
   - Booking confirmed → Driver assigned → Pickup → In transit → Delivery
   - Timestamps for each event

5. **Action Buttons**
   - Download POD (Proof of Delivery)
   - Raise issue/dispute
   - Rate driver

---

### 4.4 Driver Dashboard (Mobile-First)

**Route:** `/driver/dashboard`
**Purpose:** Driver's central hub for job management

```typescript
interface DriverStats {
  todayEarnings: number;
  weeklyEarnings: number;
  monthlyEarnings: number;
  completionRate: number;
  rating: number;
  totalJobs: number;
}

interface JobRequest {
  id: string;
  pickup: string;
  delivery: string;
  distance: number;
  materialType: string;
  weight: number;
  offeredPrice: number;
  expiresAt: Date; // 5-minute timer
}
```

**UI Components:**

1. **Earnings Summary Card**
   - Today's earnings (prominent)
   - Weekly earnings trend mini-chart
   - Monthly target progress bar

2. **Availability Toggle**
   - Large switch: "Available for Jobs" / "Offline"
   - Status indicator (green/red)

3. **Active Job Section** (if any)
   - Current pickup/delivery addresses
   - Navigation button (opens Google Maps)
   - Update status buttons:
     - "Arrived at Pickup"
     - "Loading Complete"
     - "On the Way"
     - "Arrived at Delivery"
     - "Delivery Complete"
   - Upload POD photo

4. **Job Requests** (when available)
   - Swipeable card stack
   - Show: Route, distance, material, price
   - Two buttons: ✅ Accept / ❌ Decline
   - 5-minute countdown timer
   - Auto-decline on expiry

5. **Quick Stats**
   - Rating (stars)
   - Completion rate %
   - Total jobs completed

---

### 4.5 Admin Dashboard

**Route:** `/admin/dashboard`
**Purpose:** Operations control center

**Widgets Grid:**

1. **Real-time Demand Heatmap**
   - Map showing booking density by region
   - Color-coded: Low (green) → High (red) demand
   - Hourly/daily toggle

2. **Fleet Utilization Gauge**
   - Current utilization % (target: 85%+)
   - Vehicle breakdown by type
   - Idle vs Active vs In-maintenance

3. **Live Operations Feed**
   - Real-time booking events
   - New booking → Driver assigned → In transit → Complete
   - Auto-scrolling list

4. **Pricing Override Panel**
   - Current surge multiplier by zone
   - Manual override controls
   - Scenario surcharge settings

5. **Key Metrics Cards**
   - Active bookings
   - Pending driver assignments
   - Average matching time
   - Revenue today
   - Customer satisfaction score

6. **Dispute Management**
   - Open disputes count
   - Average resolution time
   - Priority flag indicator

---

## 5. Component Specifications

### 5.1 LiveMap Component

```typescript
interface LiveMapProps {
  vehicles: Vehicle[];
  selectedVehicle?: string;
  onVehicleSelect?: (id: string) => void;
  showHeatmap?: boolean;
  showTraffic?: boolean;
  center?: [number, number];
  zoom?: number;
}

// Features:
// - Real-time vehicle markers with rotation (direction)
// - Custom popup with vehicle info on click
// - Clustering for multiple vehicles in same area
// - Heatmap layer for demand visualization
// - Route polylines for active bookings
// - Traffic overlay toggle
```

**Implementation Notes:**
- Use Mapbox GL JS for performance
- Vehicle markers as custom HTML elements
- Update positions via WebSocket (30s intervals)
- Smooth animations for position changes

---

### 5.2 PriceCard Component

```typescript
interface PriceCardProps {
  basePrice: number;
  scenarioSurcharge: number;
  platformFee: number;
  gstAmount: number;
  totalPrice: number;
  marketComparison?: {
    marketRate: number;
    savings: number;
    savingsPercent: number;
  };
  expiresAt?: Date;
  onLockPrice?: () => void;
}

// UI Breakdown:
// ┌─────────────────────────────────────┐
// │  AI-Generated Price Estimate        │
// ├─────────────────────────────────────┤
// │  Base Cost:              ₹12,500    │
// │  Festival Surcharge:     +₹2,500    │
// │  Platform Fee (4%):      +₹600     │
// │  GST (18%):              +₹2,808    │
// ├─────────────────────────────────────┤
// │  TOTAL:                  ₹18,408    │
// ├─────────────────────────────────────┤
// │  vs Market Rate: ₹22,000            │
// │  YOU SAVE: ₹3,592 (16%)              │
// ├─────────────────────────────────────┤
// │  [LOCK PRICE - 28:45 remaining]   │
// └─────────────────────────────────────┘
```

---

### 5.3 Timeline Component

```typescript
interface TimelineProps {
  events: TimelineEvent[];
  currentStatus: BookingStatus;
}

// Visual Design:
// ●─── Booking Confirmed (10:30 AM)
// │
// ●─── Driver Assigned (10:45 AM)
// │
// ○─── Pickup Complete (Pending)
// │
// ○─── In Transit (Pending)
// │
// ○─── Delivered (Pending)

// ● = completed (green)
// ○ = pending (gray)
// ⟳ = in progress (blue with pulse)
```

---

## 6. State Management Architecture

### 6.1 Zustand Stores

```typescript
// stores/authStore.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  userType: 'customer' | 'driver' | 'admin' | null;
  
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  updateProfile: (data: Partial<User>) => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      userType: null,
      
      login: async (credentials) => {
        const response = await api.auth.login(credentials);
        set({
          user: response.user,
          token: response.token,
          isAuthenticated: true,
          userType: response.user.type,
        });
      },
      
      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          userType: null,
        });
      },
      
      updateProfile: async (data) => {
        const response = await api.users.update(data);
        set({ user: response });
      },
    }),
    { name: 'auth-storage' }
  )
);
```

```typescript
// stores/bookingStore.ts
interface BookingState {
  currentBooking: BookingFormData | null;
  priceEstimate: PriceEstimate | null;
  
  setBookingData: (data: Partial<BookingFormData>) => void;
  getPriceEstimate: () => Promise<void>;
  submitBooking: () => Promise<Booking>;
  reset: () => void;
}

export const useBookingStore = create<BookingState>((set, get) => ({
  currentBooking: null,
  priceEstimate: null,
  
  setBookingData: (data) => set((state) => ({
    currentBooking: { ...state.currentBooking, ...data }
  })),
  
  getPriceEstimate: async () => {
    const { currentBooking } = get();
    const estimate = await api.pricing.estimate(currentBooking);
    set({ priceEstimate: estimate });
  },
  
  submitBooking: async () => {
    const { currentBooking } = get();
    const booking = await api.bookings.create(currentBooking);
    return booking;
  },
  
  reset: () => set({ currentBooking: null, priceEstimate: null }),
}));
```

---

### 6.2 React Query Setup

```typescript
// lib/queryClient.ts
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
})

// hooks/useBookings.ts
export function useBookings() {
  return useQuery({
    queryKey: ['bookings'],
    queryFn: () => api.bookings.getAll(),
  });
}

export function useBooking(id: string) {
  return useQuery({
    queryKey: ['booking', id],
    queryFn: () => api.bookings.getById(id),
    refetchInterval: 30000, // 30s for live tracking
  });
}

export function useCreateBooking() {
  return useMutation({
    mutationFn: api.bookings.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['bookings'] });
    },
  });
}
```

---

## 7. Real-time Integration (Socket.io)

```typescript
// lib/socket.ts
import { io } from 'socket.io-client'

export const socket = io(import.meta.env.VITE_WS_URL, {
  autoConnect: false,
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
});

// hooks/useSocket.ts
export function useSocket(event: string, callback: (data: any) => void) {
  useEffect(() => {
    socket.connect();
    socket.on(event, callback);
    
    return () => {
      socket.off(event, callback);
      socket.disconnect();
    };
  }, [event, callback]);
}

// hooks/useTracking.ts
export function useTracking(bookingId: string) {
  const [position, setPosition] = useState<GeoPoint | null>(null);
  
  useSocket(`tracking:${bookingId}`, (data) => {
    setPosition(data.position);
  });
  
  return { position };
}

// hooks/useDriverJobs.ts
export function useDriverJobs(driverId: string) {
  const [jobRequest, setJobRequest] = useState<JobRequest | null>(null);
  
  useSocket(`job:request:${driverId}`, (data) => {
    setJobRequest(data);
    // Play notification sound
    new Audio('/notification.mp3').play();
  });
  
  const acceptJob = () => {
    socket.emit('job:accept', { jobId: jobRequest?.id });
    setJobRequest(null);
  };
  
  const declineJob = () => {
    socket.emit('job:decline', { jobId: jobRequest?.id });
    setJobRequest(null);
  };
  
  return { jobRequest, acceptJob, declineJob };
}
```

**Socket Events:**

| Event | Direction | Payload | Description |
|-------|-----------|---------|-------------|
| `booking:created` | Server → Client | Booking object | New booking notification |
| `booking:assigned` | Server → Client | {bookingId, driverId} | Driver assignment |
| `booking:status` | Server → Client | {bookingId, status} | Status update |
| `tracking:update` | Server → Client | {bookingId, position} | GPS position |
| `job:request` | Server → Client | JobRequest object | New job for driver |
| `job:accept` | Client → Server | {jobId} | Driver accepts |
| `job:decline` | Client → Server | {jobId} | Driver declines |
| `price:lock` | Client → Server | {bookingId} | Lock price offer |

---

## 8. API Integration Layer

```typescript
// api/client.ts
import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add auth token
apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor - handle errors
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

---

## 9. Responsive Design System

### 9.1 Breakpoints

```typescript
// Tailwind defaults + custom
const breakpoints = {
  sm: '640px',   // Mobile landscape
  md: '768px',   // Tablet
  lg: '1024px',  // Small desktop
  xl: '1280px',  // Desktop
  '2xl': '1536px', // Large desktop
};
```

### 9.2 Mobile-First Patterns

```tsx
// Container
<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

// Grid layouts
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

// Responsive typography
<h1 className="text-2xl md:text-3xl lg:text-4xl font-bold">

// Responsive navigation
<nav className="hidden md:flex">...</nav>
<MobileMenu className="md:hidden">...</MobileMenu>

// Touch targets (min 44px)
<button className="px-4 py-3 min-h-[44px]">
```

### 9.3 Driver App Mobile Optimizations

- Bottom navigation bar (thumb-friendly)
- Large touch targets (56px minimum)
- Swipe gestures for job cards
- Pull-to-refresh for earnings
- Native map integration (deep links)
- Push notification support

---

## 10. Performance Optimization

### 10.1 Code Splitting

```typescript
// App.tsx with lazy loading
import { lazy, Suspense } from 'react'

const CustomerDashboard = lazy(() => import('./pages/customer/Dashboard'));
const DriverDashboard = lazy(() => import('./pages/driver/Dashboard'));
const AdminDashboard = lazy(() => import('./pages/admin/Dashboard'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/customer/*" element={<CustomerRoutes />} />
        <Route path="/driver/*" element={<DriverRoutes />} />
        <Route path="/admin/*" element={<AdminRoutes />} />
      </Routes>
    </Suspense>
  );
}
```

### 10.2 Image Optimization

```typescript
// Use WebP format with fallbacks
<picture>
  <source srcSet="/truck.webp" type="image/webp" />
  <img src="/truck.jpg" alt="Delivery truck" loading="lazy" />
</picture>
```

### 10.3 Map Performance

- Lazy load map component
- Debounce map movements (300ms)
- Use Mapbox vector tiles (smaller than raster)
- Cluster markers at zoom levels < 10
- Unload off-screen map layers

---

## 11. Testing Strategy

### 11.1 Test Structure

```
src/
├── __tests__/
│   ├── components/
│   │   ├── Button.test.tsx
│   │   ├── PriceCard.test.tsx
│   │   └── LiveMap.test.tsx
│   ├── hooks/
│   │   ├── useAuth.test.ts
│   │   └── usePricing.test.ts
│   ├── pages/
│   │   ├── Dashboard.test.tsx
│   │   └── NewBooking.test.tsx
│   └── integration/
│       ├── booking-flow.test.tsx
│       └── driver-job-flow.test.tsx
```

### 11.2 Example Test

```typescript
// __tests__/components/PriceCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { PriceCard } from '@/components/ui/PriceCard'

describe('PriceCard', () => {
  const mockProps = {
    basePrice: 12500,
    scenarioSurcharge: 2500,
    platformFee: 600,
    gstAmount: 2808,
    totalPrice: 18408,
    marketComparison: {
      marketRate: 22000,
      savings: 3592,
      savingsPercent: 16,
    },
    onLockPrice: vi.fn(),
  };

  it('renders price breakdown correctly', () => {
    render(<PriceCard {...mockProps} />);
    expect(screen.getByText('₹18,408')).toBeInTheDocument();
    expect(screen.getByText('YOU SAVE: ₹3,592')).toBeInTheDocument();
  });

  it('calls onLockPrice when button clicked', () => {
    render(<PriceCard {...mockProps} />);
    fireEvent.click(screen.getByText('LOCK PRICE'));
    expect(mockProps.onLockPrice).toHaveBeenCalled();
  });
});
```

---

## 12. Security Considerations

### 12.1 Authentication Flow

```typescript
// Protected route wrapper
function ProtectedRoute({ children, allowedRoles }: ProtectedRouteProps) {
  const { isAuthenticated, userType } = useAuthStore();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  if (allowedRoles && !allowedRoles.includes(userType)) {
    return <Navigate to="/unauthorized" replace />;
  }
  
  return <>{children}</>;
}

// Usage in router
<Route path="/customer/*" element={
  <ProtectedRoute allowedRoles={['customer']}>
    <CustomerLayout />
  </ProtectedRoute>
} />
```

### 12.2 Data Protection

- No sensitive data in localStorage (use httpOnly cookies)
- Input sanitization for all forms
- Rate limiting indicators in UI
- HTTPS only (enforced)
- Content Security Policy headers

---

## 13. Environment Configuration

```bash
# .env.development
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000
VITE_MAPBOX_TOKEN=pk.eyJ1IjoiemlwcHk...
VITE_GOOGLE_MAPS_KEY=AIzaSy...
VITE_APP_NAME=Zippy Logitech
VITE_APP_VERSION=1.0.0

# .env.production
VITE_API_URL=https://api.zippylogitech.in/api/v1
VITE_WS_URL=wss://api.zippylogitech.in
VITE_MAPBOX_TOKEN=pk.eyJ1IjoiemlwcHk...
VITE_GOOGLE_MAPS_KEY=AIzaSy...
VITE_SENTRY_DSN=https://...
```

---

## 14. Deployment Checklist

### 14.1 Build & Bundle

```bash
# Install dependencies
npm ci

# Run tests
npm run test

# Build for production
npm run build

# Output: dist/ folder with optimized assets
```

### 14.2 Nginx Configuration

```nginx
server {
    listen 80;
    server_name app.zippylogitech.in;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
    
    # Static assets caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # SPA fallback
    location / {
        root /var/www/zippy-frontend;
        try_files $uri $uri/ /index.html;
    }
    
    # API proxy
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 15. Development Timeline

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| **Week 1** | 5 days | Project setup, auth system, base UI components |
| **Week 2** | 5 days | Customer dashboard, booking form, pricing UI |
| **Week 3** | 5 days | Live tracking, map integration, timeline |
| **Week 4** | 5 days | Driver app (mobile-first), job requests, earnings |
| **Week 5** | 5 days | Admin panel, analytics, pricing controls |
| **Week 6** | 5 days | Testing, bug fixes, performance optimization |

**Total: 6 weeks for complete frontend**

---

## 16. Integration with Backend

| Backend Component | Frontend Integration | Status |
|-------------------|---------------------|--------|
| FastAPI REST API | Axios + React Query | ✅ Planned |
| WebSocket (Socket.io) | Real-time tracking + jobs | ✅ Planned |
| PostgreSQL | Via API layer | ✅ Indirect |
| Redis Cache | Via API layer | ✅ Indirect |
| Kafka Streams | Via WebSocket | ✅ Planned |
| ML Prediction API | Pricing estimates | ✅ Planned |
| OR-Tools Routing | Route display | ✅ Planned |
| Telegram Bot | Notification channel | ✅ Compatible |

---

*Document Version: 1.0*
*Last Updated: April 2026*
*Total Specifications: ~600 lines*
