All projects
Ai Logitech
# Driver Mobile App - Frontend Specification ## 1. Application Architecture & Navigation ### 1.1 Navigation Structure - **Primary Navigation**: Bottom tab bar with 5 main sections - Home - Orders - Inventory - Notifications - Profile/Settings - **Secondary Navigation**: Stack navigation within each tab - **Modal Navigation**: For order acceptance/rejection, document viewing, and messaging ### 1.2 Screen Hierarchy ``` App ├── Auth Stack │ ├── Login │ └── Registration ├── Main App (Bottom Tab Navigator) │ ├── Home │ ├── Orders │ │ ├── Current Order │ │ └── Order History │ ├── Inventory │ ├── Notifications │ └── Profile/Settings │ ├── Profile │ ├── Vehicle Management │ └── Settings ├── Modals │ ├── Order Details │ ├── Document Viewer │ └── Admin Messaging └── Active Navigation (Full-screen when on active order) ``` ## 2. Screen Specifications ### 2.1 Home Screen #### Components: - **Header**: App logo, notification bell icon with badge count - **Vehicle Status Card**: - Current vehicle name/number - Online/Offline toggle switch - Current location (if online) - "Change Vehicle" button (navigates to Settings) - **Quick Stats**: - Today's earnings - Orders completed today - Active order status (if any) - **Action Buttons**: - "View Orders" button - "Check Inventory" button - **Footer**: Version info, help button #### Interactions: - Toggle switch changes vehicle status with confirmation modal - "Change Vehicle" navigates to Settings with vehicle selection - Quick stats are tappable to view detailed breakdowns #### Enhancement: - Add a quick "Emergency" button for immediate assistance - Include weather information relevant to driving conditions ### 2.2 Profile Screen #### Components: - **Profile Photo**: Uploadable avatar - **Personal Information Form**: - Name (text input) - Birth date (date picker) - Mobile number (text input with validation) - Email (optional, text input with validation) - Address (text input with autocomplete) - **Professional Information**: - Vehicle type (dropdown: HCV, MCV, LCV) - Years of experience (number input) - Driver status (radio buttons: "Salaried Driver", "Vehicle Owner") - **Save Button**: At bottom of screen #### Interactions: - Form validation before saving - Success/error toast notifications - Profile photo upload with cropping functionality #### Enhancement: - Add document verification status indicators - Include driver rating display - Add "View Public Profile" option to see how profile appears to customers ### 2.3 Order Screen #### Components: - **Tab Bar**: "Current Order" and "Order History" tabs - **Current Order Tab**: - Order status indicator (with color coding) - Consignor details card - Consignee details card - Shipment value with commission breakdown - Payment status indicator - Document section with download/view options - Action buttons (Accept/Reject/Cancel) - **Order History Tab**: - Date range selector (default: past 7 days) - Filter options (completed, cancelled, rejected) - Order list with summary information - Statistics summary (accepted, rejected, cancelled counts) #### Interactions: - Order details expandable to show more information - Swipe actions on order history items for quick actions - Pull to refresh functionality #### Enhancement: - Add order search functionality - Include estimated earnings for upcoming orders - Add ability to favorite frequently visited destinations ### 2.4 Payment Transaction Screen #### Components: - **Payment Summary Card**: - Total earnings - Pending payments - Commission deducted - **Transaction List**: - Date - Order ID - Amount - Status (paid, pending, failed) - **Filter Options**: - Date range - Payment status - **Withdrawal Button**: - Available balance - "Withdraw" button with bank account selection #### Interactions: - Transaction items expandable to show details - Pull to refresh - Export transaction history option #### Enhancement: - Add payment method management - Include tax information and reports - Add payment analytics visualization ### 2.5 Inventory Status Screen #### Components: - **Vehicle Status Cards**: - In Transition vehicles list - Online vehicles list - Offline vehicles list - **Status Indicators**: - Color-coded status badges - Last seen timestamp - Current location (if available) - **Filter/Sort Options**: - By status - By vehicle type - By location #### Interactions: - Vehicle cards tappable to view details - Pull to refresh - Real-time status updates #### Enhancement: - Add vehicle utilization metrics - Include maintenance status indicators - Add map view showing all vehicle locations ### 2.6 Notification Screen #### Components: - **Notification List**: - Icon indicating notification type - Title and message - Timestamp - Read/unread indicator - **Filter Tabs**: - All - Orders - Payments - System - **Search Bar**: For finding specific notifications #### Interactions: - Mark as read/unread functionality - Swipe to delete - Pull to refresh - Tap to view details or take action #### Enhancement: - Add notification preferences - Include push notification settings - Add notification history with export option ### 2.7 Settings Screen #### Components: - **Profile Section**: - "Edit Profile" button - Profile summary - **Vehicle Management Section**: - List of registered vehicles - "Add New Vehicle" button - Vehicle status toggles - **App Preferences**: - Language selection - Theme selection (light/dark) - Notification settings - **Support Section**: - Help/FAQ - Contact Support - Terms and Conditions - Privacy Policy - **Account Actions**: - Logout button - Delete Account option #### Interactions: - Vehicle items tappable to edit details - Toggle switches for immediate status changes - Settings persist across app sessions #### Enhancement: - Add data usage settings - Include backup/restore options - Add security settings (PIN, biometrics) ## 3. Order Management Flow ### 3.1 Order Reception - **Push Notification**: New order alert with sound - **Order Modal**: - Order summary - Pickup and delivery locations - Shipment value and commission - Time estimate - Accept/Reject buttons with countdown timer ### 3.2 Order Acceptance - **Confirmation Screen**: - Detailed order information - Customer contact details - Special instructions - Document requirements - "Start Trip" button ### 3.3 Active Order Management - **Navigation Screen**: - Turn-by-turn navigation - Order progress tracker - ETA display - Customer contact buttons - Status update buttons - Emergency button ### 3.4 Document Management - **Document Scanner**: - Camera integration for document scanning - Image enhancement capabilities - Document categorization - Upload progress indicators ### 3.5 Order Completion - **Completion Screen**: - POD capture requirement - Delivery confirmation - Payment status update - Rating prompt - "Complete Order" button ## 4. Transport Company Integration Enhancements ### 4.1 Order Dashboard Updates - **Provider Type Badge**: Visual indicator for order source - **Company Branding**: Display transport company logo for affiliated orders - **Earnings Breakdown**: Clear distinction between direct and company orders - **Company Communication**: Dedicated channel for company-specific messages ### 4.2 Vehicle Management Updates - **Ownership Indicators**: Visual distinction between personal and company vehicles - **Company Sync**: Option to sync with company fleet management - **Maintenance Integration**: Company maintenance schedule visibility - **Shared Vehicle Support**: Interface for vehicle sharing arrangements ## 5. Cross-Cutting Features ### 5.1 User Identity System - **Role Switcher**: Interface for switching between driver, customer, and company roles - **Unified Profile**: Consistent profile information across roles - **Role-Specific Features**: Dynamic UI based on active role ### 5.2 Notification System - **Cross-Platform Sync**: Notification status sync across devices - **Smart Filtering**: Role-based notification filtering - **Actionable Notifications**: Direct actions from notification panel ### 5.3 Rating System - **Multi-Role Ratings**: Separate rating profiles for different roles - **Company Ratings**: Transport company rating interface - **Driver-Company Linkage**: Connected rating system for drivers and companies ## 6. Technical Specifications ### 6.1 Component Library - **Base Components**: Standardized buttons, inputs, cards, etc. - **Business Components**: Specialized components for order management, vehicle status, etc. - **Layout Components**: Navigation, headers, footers, etc. ### 6.2 State Management - **Global State**: User profile, vehicle status, active orders - **Local State**: Form inputs, UI states, temporary data - **Persistence**: Critical data stored locally for offline functionality ### 6.3 API Integration - **Authentication**: Token-based authentication with refresh mechanism - **Data Synchronization**: Background sync for critical data - **Offline Support**: Local storage with conflict resolution ### 6.4 Performance Considerations - **Image Optimization**: Compression and caching for document images - **Lazy Loading**: Progressive loading of order history and notifications - **Background Processing**: Location tracking and data sync optimization ## 7. UI/UX Guidelines ### 7.1 Design System - **Color Palette**: Primary, secondary, and status colors - **Typography**: Font families, sizes, and weights - **Iconography**: Consistent icon set for actions and status - **Spacing**: Standardized margins and padding ### 7.2 Responsive Design - **Screen Adaptation**: Layout adjustments for different screen sizes - **Touch Targets**: Minimum touch target sizes for accessibility - **Orientation Support**: Optimized layouts for portrait and landscape ### 7.3 Accessibility - **Screen Reader Support**: Labels and hints for UI elements - **High Contrast Mode**: Alternative color scheme for visibility - **Voice Commands**: Key functionality accessible via voice ## 8. Enhanced Features ### 8.1 Route Optimization - **Multiple Route Options**: Display of alternative routes with time estimates - **Traffic Integration**: Real-time traffic data integration - **Waypoint Management**: Ability to add and manage multiple stops ### 8.2 Geofencing - **Location Alerts**: Notifications for prolonged stops - **Geofenced Areas**: Visual indicators for restricted zones - **ETA Accuracy**: Improved estimates based on traffic patterns ### 8.3 Document Management - **OCR Integration**: Text extraction from documents - **Document Templates**: Pre-filled templates for common documents - **Cloud Storage**: Secure cloud backup of important documents ### 8.4 Communication Hub - **In-App Messaging**: Direct messaging with customers and admin - **Voice Notes**: Ability to send and receive voice messages - **Emergency Contacts**: Quick access to emergency contacts This frontend specification provides a comprehensive guide for developing the driver mobile application with clear UI/UX requirements, component specifications, and enhanced features. It maintains the core functionality described in the original PRD while adding clarity and slight enhancements to improve the user experience and functionality. # Zippy Logistics - Customer Mobile App PRD (Frontend Specification) ## 1. Introduction & Scope ### 1.1 Document Purpose This Product Requirements Document (PRD) outlines the frontend specifications for the Zippy Logistics Customer Mobile Application. It details the user interface, user experience, features, and business logic required for the customer-facing application. ### 1.2 Target Audience This document is intended for: - Frontend Developers - UI/UX Designers - Product Managers - Quality Assurance Teams - Project Stakeholders ### 1.3 Application Scope The Customer Mobile App is designed for businesses (MSMEs, warehouses) that need to ship goods. This application serves the "Order Placeholder" role in the Zippy Logistics ecosystem. **Explicitly Out of Scope:** - Driver-specific features (route optimization, vehicle management) - Transport Company dual-role functionality (switching between supplier/purchaser) - Direct payment between transport companies - Admin-specific functionalities ## 2. User Persona ### 2.1 Registered Customer - **Role**: Business owner or logistics manager at an MSME or warehouse - **Goals**: - Quickly and reliably book shipments - Track shipments in real-time - Manage payments and invoices efficiently - Communicate with service providers when necessary - **Pain Points**: - Difficulty finding reliable transport services - Lack of real-time visibility into shipment status - Complex payment and documentation processes ## 3. Application Architecture & Navigation ### 3.1 Navigation Structure - **Primary Navigation**: Bottom tab bar with 5 main sections - Home - Book Shipment - Track Orders - Payments - Profile ### 3.2 Screen Hierarchy ``` App ├── Auth Stack │ ├── Login │ └── Registration ├── Main App (Bottom Tab Navigator) │ ├── Home │ ├── Book Shipment │ │ ├── Shipment Details Form │ │ ├── Vehicle Selection │ │ ├── Pickup/Delivery Locations │ │ ├── Payment Processing │ │ └── Order Confirmation │ ├── Track Orders │ │ ├── Active Orders │ │ └── Order History │ ├── Payments │ │ ├── Payment Hub │ │ └── Transaction History │ └── Profile │ ├── Company Profile │ ├── Address Book │ ├── Notification Settings │ └── Settings ├── Modals │ ├── Order Details │ ├── Document Viewer │ └── Communication Hub └── Order Tracking (Full-screen for active orders) ``` ## 4. Screen-by-Screen Specification ### 4.1 Registration Screen #### Components: - **Company Information Form**: - Company Name (text input, required) - Customer Category (dropdown: MSME, Warehouse, required) - Company GST or PAN Number (text input, required, format validation) - Company Phone Number (text input, required, format validation) - Company Email Address (text input, required, format validation) - **Verification**: - Email verification (OTP sent to registered email) - Phone number verification (OTP via SMS) - **Submit Button**: Disabled until all required fields are filled and verified #### Interactions: - Real-time validation for all input fields - OTP verification process with resend option - Success/error toast notifications - Automatic login after successful registration ### 4.2 Home Screen #### Components: - **Header**: Company logo, notification bell icon with badge count - **Welcome Banner**: Personalized greeting with company name - **Quick Actions**: - "Book New Shipment" primary CTA button - "Track Active Order" button (if any active orders) - **Recent Orders Summary**: - Last order status with quick access to tracking - Summary of orders in the last 7 days - **Account Status**: - Payment status indicator (if any pending payments) - Account verification status #### Interactions: - Quick action buttons navigate to respective screens - Recent orders expandable to show basic details - Swipe to refresh for recent orders ### 4.3 Book Shipment Form #### Components: - **Progress Indicator**: Shows booking steps (1. Details, 2. Vehicle, 3. Locations, 4. Payment) - **Shipment Details Section**: - Product Type (text input with autocomplete) - Shipment Description (optional text area) - Weight/Volume inputs (with unit selectors) - Special Requirements (checkboxes for fragile, hazardous, etc.) - **Vehicle Requirements Section**: - Number of Vehicles (number selector) - Vehicle Type (radio buttons: Closed Body, Open Body) - Vehicle Model/Tonnage (two-button selection: LCV/MCV/HCV or tonnage slider) - **Pickup & Delivery Section**: - Pickup Location (Consignor - pre-filled with registered address, editable) - Delivery Location (Consignee - address input with map selector) - Schedule Options (immediate, scheduled date/time) - **Consignee Information Section**: - Consignee Name (text input) - Consignee Address (linked to delivery location) - Consignee Contact (phone number input) - **Document Upload Section**: - Shipment Document Upload (optional, with file type indicators) - Camera option for document capture - **Payment Section**: - Payment Mode (radio buttons: Part Payment (min 50%), Full Payment, ToPay) - Price Estimation (based on distance, vehicle type, etc.) - **Terms & Conditions**: - Checkbox for agreement - Link to detailed terms - **Submit Button**: "Proceed to Payment" (disabled until required fields filled) #### Interactions: - Form validation before proceeding to payment - Auto-calculation of estimated cost based on inputs - Dynamic form fields based on selections - Save as draft option ### 4.4 Order Tracking Screen #### Components: - **Map View**: - Real-time vehicle location - Route visualization - Pickup and delivery markers - **Order Status Timeline**: - Order placed - Service provider assigned - Vehicle dispatched - Pickup complete - In transit - Delivered - **Service Provider Information**: - Driver details (name, phone) - Vehicle details (type, model, registration number) - Contact options (call, message) - **ETA Display**: - Estimated arrival time at destination - Distance remaining - **Action Buttons**: - Contact Service Provider - Report Issue - Cancel/Reschedule (within allowed timeframe) #### Interactions: - Map interactive with zoom/pan - Timeline items expandable for details - Real-time updates via WebSocket connection ### 4.5 Payment Hub Screen #### Components: - **Payment Summary Card**: - Total amount - Payment status - Next payment due (if applicable) - **Payment Methods Section**: - Saved payment methods - Add new payment method - **Transaction History**: - Date - Order ID - Amount - Status - Payment method - **Invoices Section**: - List of invoices - Download options #### Interactions: - Payment methods tappable to edit - Transaction items expandable for details - Invoice download functionality ### 4.6 Profile/Settings Screen #### Components: - **Company Profile Section**: - Company logo - Company details (name, category, GST/PAN) - Contact information (phone, email) - Edit button (requires email verification for changes) - **Address Book**: - Registered address - Frequently used addresses - Add/edit/delete options - **Notification Settings**: - Push notification preferences - Email notification preferences - SMS notification preferences - **Support Section**: - Help/FAQ - Contact Support - Terms and Conditions - Privacy Policy - **Account Actions**: - Logout button - Delete Account option #### Interactions: - Profile information editable with verification - Notification preferences with toggle switches - Address book with map integration ## 5. Cross-Cutting Features ### 5.1 Notification System #### Push Notifications: - Order placed confirmation - Service provider assigned - Vehicle dispatched - Pickup completed - Shipment in transit - Delivery imminent (1 hour before arrival) - Delivered confirmation - Payment issues - Admin messages #### Email Notifications: - Order confirmation with details - Invoice generation - POD copy after delivery - Payment receipts - Account status changes #### SMS Notifications: - OTP for registration/login - Critical order updates - Delivery alerts for consignee ### 5.2 Communication Hub #### Components: - **Message Thread**: Conversation history with service provider or admin - **Message Input**: Text input with attachment option - **Contact Options**: Direct call, WhatsApp integration - **Issue Categories**: Pre-defined categories for common issues #### Interactions: - Real-time messaging - Image/document sharing - Message read receipts - Escalation to admin if needed ## 6. Business Logic & Rules ### 6.1 Order Management - **Order Confirmation**: Orders are not confirmed until payment is successfully processed. - **Cancellation/Reschedule Policy**: Customers can cancel or reschedule orders within the first 30 minutes without penalty. After this period, a fee is charged based on the distance from the vehicle's current location to the consignor's location. - **Order Blocking**: Customers with outstanding payments cannot place new orders unless manually approved by an admin. - **Document Verification**: Customers must allow drivers to scan shipment documents and verify product/packaging quality. Any defects found will be documented by the driver. ### 6.2 Payment Processing - **Payment Modes**: - Part Payment: Minimum 50% advance payment required - Full Payment: 100% payment upfront - ToPay: Consignee will make the payment upon delivery - **Payment Responsibility**: The customer (consignor) is responsible for clarifying who will make the payment. - **Advance Payment**: If selected, advance payment is processed after loading is complete. - **Final Settlement**: Full payment must be settled after completion of shipment. - **Commission Structure**: Customers do not pay any commission to Zippy Logistics. Commission is deducted from the service provider (driver or transport company). ### 6.3 Shipment Tracking - **Real-time Tracking**: Customers can track vehicle movement in real-time. - **ETA Updates**: Customers receive updated estimated arrival times. - **Consignee Notifications**: The consignee receives a message one hour before the vehicle arrives at the destination. - **POD Delivery**: Customers receive the Proof of Delivery (POD) copy via email after shipment completion. - **Invoice Delivery**: If ToPay is selected, the consignee receives an invoice copy. ### 6.4 Data Management - **Transaction History**: Customers can view past payment transactions, invoice copies, and shipment destinations for the past 7 days. - **Current Order Status**: Customers can view current order details, payment transactions, vehicle tracking, ETA, and POD status. - **Profile Modification**: Customers can modify their profile contact details, but email verification is required for changes to the email address. - **Pre-booking Scheduling**: Customers can schedule shipments in advance. ## 7. Technical Considerations ### 7.1 API Integration - **Authentication**: Token-based authentication with refresh mechanism - **Real-time Updates**: WebSocket integration for live tracking and notifications - **Payment Gateway**: Integration with secure payment processing - **Map Services**: Integration with mapping service for location tracking and address selection - **Document Storage**: Cloud storage for shipment documents and invoices ### 7.2 State Management - **Global State**: User profile, active orders, payment methods - **Local State**: Form inputs, UI states, temporary data - **Persistence**: Critical data stored locally for offline functionality ### 7.3 Performance Considerations - **Image Optimization**: Compression and caching for document images - **Lazy Loading**: Progressive loading of order history and notifications - **Background Processing**: Location tracking and data sync optimization ## 8. UI/UX Guidelines ### 8.1 Design System - **Color Palette**: Primary, secondary, and status colors aligned with Zippy Logistics branding - **Typography**: Font families, sizes, and weights optimized for readability - **Iconography**: Consistent icon set for actions and status - **Spacing**: Standardized margins and padding ### 8.2 Responsive Design - **Screen Adaptation**: Layout adjustments for different screen sizes - **Touch Targets**: Minimum touch target sizes for accessibility - **Orientation Support**: Optimized layouts for portrait and landscape ### 8.3 Accessibility - **Screen Reader Support**: Labels and hints for UI elements - **High Contrast Mode**: Alternative color scheme for visibility - **Voice Commands**: Key functionality accessible via voice (where applicable) # Zippy Logistics - Transport Company Mobile App PRD (Frontend Specification) ## 1. Introduction & Scope ### 1.1 Document Purpose This Product Requirements Document (PRD) outlines the frontend specifications for the Zippy Logistics Transport Company Mobile Application. This app is designed to address the unique dual-role functionality required by transport companies who operate as both customers (order placeholders) and service providers (order receivers) within the Zippy Logistics ecosystem. ### 1.2 Target Audience This document is intended for: - Frontend Developers - UI/UX Designers - Product Managers - Quality Assurance Teams - Project Stakeholders ### 1.3 Application Scope The Transport Company Mobile App serves as a unified interface for transport businesses to: 1. Place orders when they lack sufficient vehicles (Customer role) 2. Accept orders from other companies when they have excess capacity (Provider role) 3. Manage their own fleet and resources 4. Interact with other transport companies within the platform **Explicitly Out of Scope:** - Direct payment processing between transport companies (handled externally) - Admin-specific functionalities - End-customer specific features (handled by the Customer App) ## 2. User Persona ### 2.1 Transport Company Manager - **Role**: Manager or owner of a transport company - **Goals**: - Maximize fleet utilization - Find additional orders when capacity is available - Find vehicles when resources are insufficient - Manage relationships with partner transport companies - **Pain Points**: - Difficulty balancing demand and supply - Inefficient processes for collaborating with other transport companies - Lack of visibility into market demand and available resources ## 3. Application Architecture & Navigation ### 3.1 Navigation Structure - **Primary Navigation**: Bottom tab bar with 5 main sections - Dashboard - Orders - Fleet - Network - Profile ### 3.2 Screen Hierarchy ``` App ├── Auth Stack │ ├── Login │ └── Registration ├── Main App (Bottom Tab Navigator) │ ├── Dashboard │ │ ├── Role Toggle (Customer/Provider) │ │ ├── Overview Cards │ │ └── Quick Actions │ ├── Orders │ │ ├── Customer Orders (Placed) │ │ ├── Provider Orders (Received) │ │ └── Order Details │ ├── Fleet │ │ ├── Vehicle Management │ │ ├── Driver Management │ │ └── Maintenance │ ├── Network │ │ ├── Partner Directory │ │ ├── Marketplace │ │ └── Collaboration History │ └── Profile │ ├── Company Profile │ ├── Financials │ ├── Settings │ └── Notifications ├── Modals │ ├── Order Details │ ├── Partner Details │ └── Communication Hub └── Role Switching Overlay ``` ## 4. Core Feature: Role Toggle System ### 4.1 Role Toggle Interface #### Components: - **Toggle Button**: Prominent, draggable button at the top of the dashboard - Visual design: Slider with "Customer" and "Provider" labels - Color coding: Orange for Customer (OMS), Purple for Provider (TMS) - Animation: Smooth transition with UI transformation when switching - **Role Indicator**: Persistent indicator showing current active role - **Contextual Header**: Header changes based on selected role - Customer role: "Place Orders" header - Provider role: "Find Orders" header #### Interactions: - Drag or tap to switch between roles - UI elements transform based on selected role - Data view adjusts to show relevant information for current role - Quick action buttons change based on role #### Business Logic: - Single user ID works across both roles - Notification system remains unified regardless of role - Historical data accessible in both roles with appropriate filtering - Role preference persists between sessions ## 5. Screen-by-Screen Specification ### 5.1 Dashboard Screen #### Components: - **Role Toggle Section**: As described in section 4.1 - **Overview Cards**: - Active Orders (placed and received) - Fleet Utilization (own vehicles vs. partner vehicles) - Revenue/Expenses (based on current role) - Network Activity (recent partner interactions) - **Quick Actions**: - "Place Order" (when in Customer role) - "Find Orders" (when in Provider role) - "Manage Fleet" - "Connect with Partners" - **Resource Utilization Chart**: - Visual representation of own fleet capacity - Partner vehicle utilization - Demand/supply gap visualization #### Interactions: - Role toggle transforms the dashboard view - Cards are tappable to view detailed information - Quick action buttons navigate to respective screens - Charts are interactive with filtering options ### 5.2 Orders Screen #### Components: - **Tab Navigation**: "Placed Orders" and "Received Orders" tabs - **Placed Orders Tab** (Customer role): - Order list with status indicators - Filter options (status, date, provider) - Order summary information - Quick actions (track, modify, cancel) - **Received Orders Tab** (Provider role): - Order queue with accept/reject options - Order details with requirements - Vehicle assignment interface - Order status tracking - **Order Details Modal**: - Complete order information - Communication with other party - Document access - Status timeline #### Interactions: - Tab switching shows different order perspectives - Order items expandable for details - Swipe actions for quick responses - Pull to refresh for real-time updates ### 5.3 Fleet Management Screen #### Components: - **Vehicle Inventory**: - List of own vehicles with status - Vehicle details (type, capacity, location) - Availability indicators - Maintenance status - **Driver Management**: - Driver profiles with ratings - Assignment history - Availability status - **Maintenance Schedule**: - Upcoming maintenance - Service history - Cost tracking #### Interactions: - Vehicle items tappable to view/edit details - Drag and drop for vehicle assignment - Filter and sort options - Status toggle for vehicle availability ### 5.4 Network Screen #### Components: - **Partner Directory**: - Searchable list of transport companies - Partner profiles with specialties - Reliability ratings - Collaboration history - **Marketplace**: - Posts from companies seeking vehicles - Posts from companies offering excess capacity - Filter options (location, vehicle type, volume) - **Collaboration History**: - Past interactions with partners - Performance metrics - Communication logs #### Interactions: - Partner items tappable to view details - Marketplace items expandable for more information - Quick connect options for urgent needs - Filter and search functionality ### 5.5 Profile & Financials Screen #### Components: - **Company Profile**: - Company information - Certifications and licenses - Service areas - Specializations - **Financial Management**: - Transaction history (income and expenses) - Service fee tracking (₹700 flat rate) - Invoice generation - Payment status - **Settings**: - Notification preferences - Privacy settings - Account management - **Support**: - Help center - Contact support - FAQ #### Interactions: - Editable profile fields with validation - Transaction items expandable for details - Settings with toggle switches - Search functionality in help center ## 6. Cross-Cutting Features ### 6.1 Unified Notification System #### Components: - **Notification Center**: Single notification system regardless of role - **Notification Types**: - New order requests (as provider) - Order status updates (as customer) - Partner requests and responses - Vehicle availability alerts - Payment confirmations - Service fee notifications #### Interactions: - Notifications categorized by type - Actionable notifications with quick response options - Notification settings apply across both roles - Badge count indicators ### 6.2 Communication Hub #### Components: - **Unified Messaging**: Single messaging system for all communications - **Message Threads**: Organized by partner or order - **Quick Actions**: Call, email, WhatsApp integration - **Document Sharing**: Ability to share documents within conversations #### Interactions: - Real-time messaging - Message history accessible regardless of role - File attachment capabilities - Message search functionality ### 6.3 Map Integration #### Components: - **Dual-Purpose Map**: - Customer view: Order pickup and delivery locations, vehicle tracking - Provider view: All active vehicles, demand heat map - **Partner Locations**: View of partner companies and their service areas - **Route Visualization**: Display of active routes and planned routes #### Interactions: - Map view changes based on current role - Interactive markers with detailed information - Layer toggles for different information types - Zoom and pan controls ## 7. Business Logic & Rules ### 7.1 Role Switching - Transport companies can switch between Customer and Provider roles at any time - UI transforms to show relevant features for the selected role - Data is filtered based on the current role but remains accessible - Role preference is saved between sessions ### 7.2 Order Management - As Customer: Transport companies can place orders when they lack sufficient vehicles - As Provider: Transport companies can receive orders from other companies when they have excess capacity - Orders can be transferred between transport companies based on capacity and availability - Order status updates are reflected in real-time ### 7.3 Payment Processing - Zippy charges a flat ₹700 fee to transport companies who accept orders through the platform - No commission is charged from transport companies who place orders - Payment between transport companies is handled externally (not through the app) - Service fee tracking is visible in the financial section ### 7.4 Partner Network - Transport companies can discover and connect with other companies on the platform - Collaboration history is tracked and used for reliability ratings - Preferred partners can be marked for quick access - Network activity is displayed on the dashboard ## 8. Technical Considerations ### 8.1 State Management - **Global State**: User profile, role preference, active orders, fleet data - **Local State**: Form inputs, UI states, temporary data - **Persistence**: Critical data stored locally for offline functionality - **Role Context**: State management system that handles role switching ### 8.2 API Integration - **Authentication**: Token-based authentication with refresh mechanism - **Real-time Updates**: WebSocket integration for live updates - **Role-Based Endpoints**: Different API endpoints based on current role - **Data Synchronization**: Background sync for critical data ### 8.3 Performance Considerations - **Image Optimization**: Compression and caching for profile pictures and documents - **Lazy Loading**: Progressive loading of order history and partner lists - **Background Processing**: Location tracking and data sync optimization - **Role Switching Optimization**: Efficient state management for seamless role transitions ## 9. UI/UX Guidelines ### 9.1 Design System - **Color Palette**: - Primary: Teal (#009688) for Transport Company branding - Customer Role: Orange (#FF9800) for OMS functionality - Provider Role: Purple (#9C27B0) for TMS functionality - Network: Indigo (#3F51B5) for partner connections - Service Fee: Amber (#FFC107) for fee indicators - **Typography**: Font families, sizes, and weights optimized for readability - **Iconography**: Consistent icon set for actions and status - **Spacing**: Standardized margins and padding ### 9.2 Responsive Design - **Screen Adaptation**: Layout adjustments for different screen sizes - **Touch Targets**: Minimum touch target sizes for accessibility - **Orientation Support**: Optimized layouts for portrait and landscape - **Role Adaptation**: UI adaptation based on current active role ### 9.3 Accessibility - **Screen Reader Support**: Labels and hints for UI elements - **High Contrast Mode**: Alternative color scheme for visibility - **Voice Commands**: Key functionality accessible via voice (where applicable) - **Role Indicator Accessibility**: Clear indication of current role for screen readers ## 10. Implementation Approach ### 10.1 Development Phases 1. **Phase 1**: Core functionality with basic role switching 2. **Phase 2**: Enhanced network features and partner management 3. **Phase 3**: Advanced analytics and AI integration 4. **Phase 4**: Optimization and performance enhancements ### 10.2 Testing Strategy - **Role Switching Testing**: Ensure seamless transitions between roles - **Cross-Functional Testing**: Verify all features work in both roles - **Network Testing**: Test partner discovery and collaboration features - **Performance Testing**: Ensure app performs well with large datasets ### 10.3 Success Metrics - User engagement with role switching feature - Number of inter-company collaborations - Reduction in vehicle idle time - Improvement in fleet utilization - User satisfaction with the unified interface # Zippy Logistics - Admin Dashboard PRD (Frontend Specification) ## 1. Introduction & Scope ### 1.1 Document Purpose This Product Requirements Document (PRD) outlines the frontend specifications for the Zippy Logistics Admin Dashboard. This dashboard serves as the central command center for monitoring, regulating, and guiding all participants in the Zippy Logistics ecosystem. ### 1.2 Target Audience This document is intended for: - Frontend Developers - UI/UX Designers - Product Managers - Quality Assurance Teams - Project Stakeholders ### 1.3 Application Scope The Admin Dashboard is designed to provide comprehensive oversight and control of the entire Zippy Logistics platform, including: - Real-time monitoring of all participant activities - Issue resolution and exception handling - System regulation and policy enforcement - Data analysis and predictive insights - AI agent supervision and correction **Explicitly Out of Scope**: - Direct customer service interactions (handled through separate channels) - System infrastructure management (handled by DevOps team) - Financial accounting beyond platform transactions ## 2. User Persona ### 2.1 Platform Administrator - **Role**: System administrator responsible for platform oversight - **Goals**: - Maintain platform integrity and security - Resolve technical issues efficiently - Optimize system performance - Ensure compliance with regulations - **Pain Points**: - Managing complex multi-participant ecosystem - Identifying and addressing system anomalies - Balancing automation with human oversight - Handling emergency situations effectively ## 3. Application Architecture & Navigation ### 3.1 Navigation Structure - **Primary Navigation**: Sidebar navigation with hierarchical menu - **Secondary Navigation**: Tab-based navigation within each section - **Quick Actions**: Floating action buttons for common tasks - **Breadcrumb Navigation**: Clear path indication for deep navigation ### 3.2 Screen Hierarchy ``` Admin Dashboard ├── Dashboard Overview │ ├── System Health │ ├── Activity Metrics │ ├── Alert Center │ └── Quick Actions ├── Participant Management │ ├── Customer Management │ ├── Driver Management │ ├── Transport Company Management │ └── User Analytics ├── Order Management │ ├── Order Monitoring │ ├── Order Intervention │ ├── Suspicious Order Detection │ └── Order Analytics ├── Fleet Management │ ├── Vehicle Tracking │ ├── Route Monitoring │ ├── Maintenance Oversight │ └── Utilization Analytics ├── Financial Oversight │ ├── Transaction Monitoring │ ├── Payment Issues │ ├── Refund Management │ └── Revenue Analytics ├── AI Agent Supervision │ ├── Agent Performance │ ├── Hallucination Detection │ ├── Model Retraining │ └── Algorithm Adjustment ├── Compliance & Security │ ├── Policy Enforcement │ ├── Violation Tracking │ ├── Security Monitoring │ └── Audit Logs └── System Configuration ├── Platform Settings ├── Notification Configuration ├── Alert Thresholds └── System Maintenance ``` ## 4. Screen-by-Screen Specification ### 4.1 Dashboard Overview #### Components: - **System Health Panel**: - Server status indicators - API response times - Database performance metrics - Real-time error rates - **Activity Metrics**: - Active users by type (customers, drivers, transport companies) - Order volume trends - Platform utilization rates - Geographic distribution of activities - **Alert Center**: - Critical alerts requiring immediate attention - Warning alerts for potential issues - Informational alerts for system updates - Alert history with resolution status - **Quick Actions**: - Send system-wide notifications - Emergency order cancellation - User suspension/activation - System maintenance mode toggle #### Interactions: - Real-time data refresh with configurable intervals - Drill-down capability on all metrics - Alert filtering and prioritization - Customizable dashboard layout #### Technical Implementation: - WebSocket connections for real-time data - Data visualization libraries (D3.js, Chart.js) - Responsive grid layout - State management for alert handling ### 4.2 Participant Management #### Components: - **User Directory**: - Searchable list of all platform participants - Filtering by user type, status, location - User profiles with activity history - Performance metrics and ratings - **User Analytics**: - User acquisition and retention metrics - Behavior patterns analysis - Geographic distribution visualization - Activity heat maps - **Account Actions**: - User suspension/activation - Account verification - Password reset - Profile modification permissions #### Interactions: - Advanced filtering and search capabilities - Bulk actions for multiple users - Direct messaging to users - Activity timeline for each user #### Technical Implementation: - Pagination for large user lists - Advanced search with autocomplete - Role-based access control - Activity logging for audit purposes ### 4.3 Order Management #### Components: - **Order Monitoring Dashboard**: - Real-time order status visualization - Order flow visualization - Exception highlighting - Geographic distribution of orders - **Order Intervention Tools**: - Order cancellation interface - Refund processing - Order modification capabilities - Manual driver assignment - **Suspicious Order Detection**: - AI-powered anomaly detection - Risk scoring for orders - Pattern recognition for fraudulent activities - Manual review queue - **Order Analytics**: - Booking pattern analysis - Cancellation reasons breakdown - Rejection rate analysis - Rescheduling frequency metrics #### Interactions: - Real-time order status updates - Drill-down to order details - Intervention workflow with approval steps - Customizable alert thresholds #### Technical Implementation: - Real-time data streaming - Machine learning integration for anomaly detection - Complex filtering and sorting - Export functionality for reports ### 4.4 Fleet Management #### Components: - **Vehicle Tracking Dashboard**: - Real-time map view of all vehicles - Vehicle status indicators - Route visualization - Location history playback - **Route Monitoring**: - Active route visualization - Deviation alerts - ETA accuracy tracking - Traffic impact analysis - **Maintenance Oversight**: - Maintenance schedule tracking - Service history - Compliance status - Cost analysis - **Utilization Analytics**: - Vehicle utilization rates - Idle time analysis - Performance metrics - Efficiency recommendations #### Interactions: - Interactive map with filtering options - Route playback with speed controls - Maintenance scheduling interface - Performance comparison tools #### Technical Implementation: - Mapping API integration (Google Maps, Mapbox) - Geospatial data processing - Real-time location tracking - Predictive maintenance algorithms ### 4.5 Financial Oversight #### Components: - **Transaction Monitoring**: - Real-time transaction visualization - Payment status tracking - Failed transaction analysis - Revenue metrics - **Payment Issues**: - Failed payment alerts - Refund processing queue - Dispute resolution interface - Payment gateway status - **Refund Management**: - Refund request queue - Refund policy enforcement - Refund analytics - Automated refund rules - **Revenue Analytics**: - Revenue trends - Commission tracking - Profitability analysis - Financial forecasting #### Interactions: - Transaction drill-down capabilities - Refund approval workflow - Customizable financial reports - Revenue comparison tools #### Technical Implementation: - Secure payment gateway integration - Financial data encryption - Automated fraud detection - Advanced financial analytics ### 4.6 AI Agent Supervision #### Components: - **Agent Performance Dashboard**: - Agent accuracy metrics - Response time analysis - Error rate tracking - Performance trends - **Hallucination Detection**: - Anomaly detection in AI responses - Confidence scoring - Manual review queue - Feedback collection - **Model Retraining**: - Retraining triggers - Model versioning - A/B testing interface - Performance comparison - **Algorithm Adjustment**: - Parameter tuning interface - Algorithm configuration - Rollback capabilities - Impact assessment #### Interactions: - Real-time agent monitoring - Manual override capabilities - Feedback loop implementation - Model performance comparison #### Technical Implementation: - ML model monitoring tools - Anomaly detection algorithms - A/B testing framework - Model version control ### 4.7 Compliance & Security #### Components: - **Policy Enforcement**: - Rule configuration interface - Violation tracking - Penalty management - Compliance reporting - **Violation Tracking**: - Violation detection - Evidence collection - Resolution workflow - Pattern analysis - **Security Monitoring**: - Access log analysis - Threat detection - Security incident response - Vulnerability scanning - **Audit Logs**: - Comprehensive activity logging - Log analysis tools - Compliance reporting - Data retention management #### Interactions: - Rule configuration interface - Violation review workflow - Security incident response - Audit log search and filtering #### Technical Implementation: - Security information and event management (SIEM) - Compliance automation - Advanced threat detection - Secure log storage ### 4.8 System Configuration #### Components: - **Platform Settings**: - System parameters configuration - Feature flags management - Integration settings - Performance tuning - **Notification Configuration**: - Notification templates - Delivery channels - Frequency settings - Personalization options - **Alert Thresholds**: - Customizable alert rules - Escalation paths - Notification preferences - Alert history - **System Maintenance**: - Maintenance scheduling - Backup management - Update deployment - Rollback procedures #### Interactions: - Configuration form validation - Test notification sending - Alert rule builder - Maintenance scheduling interface #### Technical Implementation: - Configuration management system - Template engine for notifications - Rule engine for alerts - Deployment pipeline integration ## 5. Cross-Cutting Features ### 5.1 Real-Time Monitoring #### Components: - **WebSocket Connections**: For real-time data updates - **Event Streaming**: For continuous data flow - **Alert System**: For immediate notification of issues - **Status Indicators**: Visual representation of system health #### Technical Implementation: - WebSocket implementation - Event-driven architecture - Push notification system - Real-time data processing ### 5.2 Data Visualization #### Components: - **Interactive Charts**: For data exploration - **Geographic Maps**: For location-based data - **Heat Maps**: For density visualization - **Trend Analysis**: For pattern recognition #### Technical Implementation: - D3.js for advanced visualizations - Chart.js for standard charts - Mapping libraries for geographic data - Custom visualization components ### 5.3 Predictive Analytics #### Components: - **Forecasting Models**: For trend prediction - **Anomaly Detection**: For issue identification - **Recommendation Engine**: For optimization suggestions - **Risk Assessment**: For threat evaluation #### Technical Implementation: - Python backend with ML frameworks - TensorFlow/PyTorch for deep learning - Scikit-learn for traditional ML - Pandas for data manipulation ## 6. Technical Architecture ### 6.1 Frontend Technology Stack - **Framework**: React.js with TypeScript - **State Management**: Redux with middleware for real-time updates - **UI Library**: Material-UI for consistent design - **Data Visualization**: D3.js, Chart.js, Recharts - **Mapping**: Mapbox or Google Maps API - **Real-time Communication**: WebSocket connections - **Testing**: Jest, React Testing Library ### 6.2 Backend Integration - **API Gateway**: For centralized API management - **Microservices**: For modular functionality - **Message Queue**: For asynchronous processing - **Database**: PostgreSQL for relational data, MongoDB for document storage - **Caching**: Redis for performance optimization - **File Storage**: AWS S3 or similar for document storage ### 6.3 AI/ML Integration - **Python Backend**: For ML model execution - **Model Serving**: TensorFlow Serving or similar - **Feature Store**: For ML feature management - **Model Monitoring**: For performance tracking - **Feedback Loop**: For continuous improvement ## 7. Security Considerations ### 7.1 Authentication & Authorization - **Multi-Factor Authentication**: For enhanced security - **Role-Based Access Control**: For permission management - **Session Management**: For secure user sessions - **API Security**: For backend protection ### 7.2 Data Protection - **Encryption**: For sensitive data protection - **Data Masking**: For privacy protection - **Audit Logging**: For accountability - **Backup & Recovery**: For data resilience ## 8. Performance Optimization ### 8.1 Frontend Optimization - **Code Splitting**: For reduced initial load time - **Lazy Loading**: For on-demand resource loading - **Caching Strategy**: For improved performance - **Bundle Optimization**: For reduced size ### 8.2 Backend Optimization - **Database Optimization**: For efficient queries - **Caching Layer**: For reduced database load - **Load Balancing**: For scalability - **CDN Integration**: For content delivery ## 9. Implementation Approach ### 9.1 Development Phases 1. **Phase 1**: Core monitoring and participant management 2. **Phase 2**: Order management and intervention tools 3. **Phase 3**: AI agent supervision and advanced analytics 4. **Phase 4**: Predictive analytics and optimization features ### 9.2 Testing Strategy - **Unit Testing**: For component validation - **Integration Testing**: For system interaction - **End-to-End Testing**: For user workflow validation - **Performance Testing**: For system scalability ### 9.3 Success Metrics - System uptime and availability - Issue resolution time - User satisfaction with admin tools - Reduction in manual intervention needs - Accuracy of AI predictions and recommendations ## 10. Maintenance & Evolution ### 10.1 Monitoring & Alerting - **System Health Monitoring**: For proactive issue detection - **Performance Metrics**: For optimization opportunities - **Error Tracking**: For rapid issue resolution - **Usage Analytics**: For feature improvement ### 10.2 Continuous Improvement - **User Feedback**: For feature enhancement - **A/B Testing**: For optimization - **Performance Analysis**: For system tuning - **Security Updates**: For vulnerability protection # Backend PRD - Refined for 7-Agent Architecture After reviewing the 7-agent architecture against the existing backend PRD, I've identified key areas that need refinement to fully support the agent-based system. The following adjustments ensure the backend properly supports all agent interactions and workflows. ## 1. Agent Service Layer Architecture ### 1.1 Agent Service Base Class ```python # apps/agents/services.py from abc import ABC, abstractmethod from django.db import transaction from django.utils import timezone import logging logger = logging.getLogger(__name__) class BaseAgentService(ABC): """Base class for all agent services""" def __init__(self): self.agent_name = self.__class__.__name__.replace('Service', '').lower() self.logger = logging.getLogger(f'agents.{self.agent_name}') @abstractmethod def process_task(self, task_data): """Process a task assigned to this agent""" pass def log_activity(self, action, details, user=None): """Log agent activity""" from apps.agents.models import AgentActivityLog AgentActivityLog.objects.create( agent_name=self.agent_name, action=action, details=details, user=user, timestamp=timezone.now() ) def communicate_with_agent(self, target_agent, message_data): """Send message to another agent""" from apps.agents.utils import AgentCommunicator communicator = AgentCommunicator() return communicator.send_message( from_agent=self.agent_name, to_agent=target_agent, message_data=message_data ) ``` ### 1.2 Agent Communication Infrastructure ```python # apps/agents/utils.py import redis import json from django.conf import settings from celery import shared_task class AgentCommunicator: """Handles communication between agents""" def __init__(self): self.redis_client = redis.Redis.from_url(settings.REDIS_URL) self.message_queue = "agent_messages" def send_message(self, from_agent, to_agent, message_data): """Send message from one agent to another""" message = { 'from_agent': from_agent, 'to_agent': to_agent, 'message_data': message_data, 'timestamp': timezone.now().isoformat(), 'message_id': str(uuid.uuid4()) } # Store in Redis queue self.redis_client.lpush(self.message_queue, json.dumps(message)) # Log the communication from apps.agents.models import AgentCommunicationLog AgentCommunicationLog.objects.create( from_agent=from_agent, to_agent=to_agent, message_data=message_data, message_id=message['message_id'] ) return message['message_id'] def get_messages(self, agent_name): """Get messages for a specific agent""" messages = [] queue_length = self.redis_client.llen(self.message_queue) for _ in range(queue_length): message_data = self.redis_client.rpop(self.message_queue) if message_data: message = json.loads(message_data) if message['to_agent'] == agent_name: messages.append(message) return messages @shared_task def process_agent_messages(): """Background task to process agent messages""" communicator = AgentCommunicator() # Get all active agents from apps.agents.models import ActiveAgent active_agents = ActiveAgent.objects.filter(is_active=True) for agent in active_agents: messages = communicator.get_messages(agent.agent_name) for message in messages: # Process each message from apps.agents.registry import get_agent_service service = get_agent_service(agent.agent_name) if service: service.handle_message(message) ``` ## 2. Agent-Specific Service Implementations ### 2.1 Customer Service Agent Implementation ```python # apps/agents/customer_service.py from .services import BaseAgentService from apps.orders.models import Order from apps.users.models import User from apps.communication.utils import send_notification class CustomerServiceAgentService(BaseAgentService): """Service for Customer Service Agent""" def process_task(self, task_data): """Process customer service tasks""" task_type = task_data.get('task_type') if task_type == 'handle_inquiry': return self.handle_customer_inquiry(task_data) elif task_type == 'process_order_request': return self.process_order_request(task_data) elif task_type == 'resolve_issue': return self.resolve_customer_issue(task_data) else: self.logger.warning(f"Unknown task type: {task_type}") return {'status': 'error', 'message': 'Unknown task type'} def handle_customer_inquiry(self, inquiry_data): """Handle customer inquiry""" customer_id = inquiry_data.get('customer_id') inquiry_type = inquiry_data.get('inquiry_type') inquiry_text = inquiry_data.get('inquiry_text') try: customer = User.objects.get(id=customer_id) # Log the inquiry self.log_activity( action='inquiry_received', details={ 'customer_id': customer_id, 'inquiry_type': inquiry_type, 'inquiry_text': inquiry_text }, user=customer ) # Process inquiry based on type if inquiry_type == 'order_status': return self.handle_order_status_inquiry(customer, inquiry_data) elif inquiry_type == 'payment_issue': return self.handle_payment_inquiry(customer, inquiry_data) elif inquiry_type == 'general': return self.handle_general_inquiry(customer, inquiry_data) except User.DoesNotExist: self.logger.error(f"Customer not found: {customer_id}") return {'status': 'error', 'message': 'Customer not found'} def process_order_request(self, order_data): """Process new order request from customer""" customer_id = order_data.get('customer_id') try: customer = User.objects.get(id=customer_id) # Create order order = Order.objects.create( customer=customer, pickup_location=order_data.get('pickup_location'), delivery_location=order_data.get('delivery_location'), cargo_details=order_data.get('cargo_details'), status='pending' ) # Log order creation self.log_activity( action='order_created', details={'order_id': str(order.id)}, user=customer ) # Communicate with Order Management Agent self.communicate_with_agent( target_agent='order_management', message_data={ 'task_type': 'process_new_order', 'order_id': str(order.id) } ) return { 'status': 'success', 'order_id': str(order.id), 'message': 'Order created successfully' } except User.DoesNotExist: self.logger.error(f"Customer not found: {customer_id}") return {'status': 'error', 'message': 'Customer not found'} def handle_message(self, message): """Handle incoming message from another agent""" message_data = message.get('message_data') if message_data.get('task_type') == 'order_update_notification': return self.send_order_update_notification(message_data) elif message_data.get('task_type') == 'payment_confirmation': return self.send_payment_confirmation(message_data) return {'status': 'success'} ``` ### 2.2 Order Management Agent Implementation ```python # apps/agents/order_management.py from .services import BaseAgentService from apps.orders.models import Order from apps.orders.services import OrderLifecycleService, PaymentService from apps.agents.resource_management import ResourceManagementAgentService class OrderManagementAgentService(BaseAgentService): """Service for Order Management Agent""" def __init__(self): super().__init__() self.lifecycle_service = OrderLifecycleService() self.payment_service = PaymentService() self.resource_service = ResourceManagementAgentService() def process_task(self, task_data): """Process order management tasks""" task_type = task_data.get('task_type') if task_type == 'process_new_order': return self.process_new_order(task_data) elif task_type == 'assign_provider': return self.assign_provider_to_order(task_data) elif task_type == 'update_order_status': return self.update_order_status(task_data) elif task_type == 'handle_payment_confirmation': return self.handle_payment_confirmation(task_data) else: self.logger.warning(f"Unknown task type: {task_type}") return {'status': 'error', 'message': 'Unknown task type'} def process_new_order(self, order_data): """Process new order from Customer Service Agent""" order_id = order_data.get('order_id') try: order = Order.objects.get(id=order_id) # Validate order validation_result = self.validate_order(order) if not validation_result['valid']: return { 'status': 'error', 'message': validation_result['message'] } # Calculate pricing pricing_result = self.calculate_pricing(order) order.base_amount = pricing_result['base_amount'] order.total_amount = pricing_result['total_amount'] order.save() # Check resource availability availability_result = self.resource_service.check_availability(order) if not availability_result['available']: return { 'status': 'error', 'message': 'No available resources', 'alternatives': availability_result.get('alternatives', []) } # Update order status self.lifecycle_service.transition_status( order_id=order_id, new_status='inventory_confirmed', user=None ) # Communicate with Payment & Settlement Agent self.communicate_with_agent( target_agent='payment_settlement', message_data={ 'task_type': 'initiate_payment', 'order_id': str(order.id), 'amount': float(order.total_amount) } ) return { 'status': 'success', 'order_id': str(order.id), 'total_amount': float(order.total_amount), 'message': 'Order processed successfully' } except Order.DoesNotExist: self.logger.error(f"Order not found: {order_id}") return {'status': 'error', 'message': 'Order not found'} def assign_provider_to_order(self, assignment_data): """Assign provider to order""" order_id = assignment_data.get('order_id') try: order = Order.objects.get(id=order_id) # Get available providers providers = self.resource_service.get_available_providers(order) if not providers: return { 'status': 'error', 'message': 'No available providers' } # Select best provider best_provider = self.select_best_provider(providers, order) # Assign provider to order order.provider = best_provider['user'] order.provider_type = best_provider['type'] order.status = 'driver_assigned' order.save() # Update provider availability self.resource_service.update_provider_availability( provider_id=best_provider['user'].id, availability=False ) # Communicate with Transportation Agent self.communicate_with_agent( target_agent='transportation', message_data={ 'task_type': 'initiate_transportation', 'order_id': str(order.id), 'provider_id': str(best_provider['user'].id) } ) # Communicate with Customer Service Agent self.communicate_with_agent( target_agent='customer_service', message_data={ 'task_type': 'order_update_notification', 'order_id': str(order.id), 'status': 'driver_assigned', 'provider_details': best_provider } ) return { 'status': 'success', 'order_id': str(order.id), 'provider_id': str(best_provider['user'].id), 'message': 'Provider assigned successfully' } except Order.DoesNotExist: self.logger.error(f"Order not found: {order_id}") return {'status': 'error', 'message': 'Order not found'} def handle_message(self, message): """Handle incoming message from another agent""" message_data = message.get('message_data') if message_data.get('task_type') == 'payment_completed': return self.handle_payment_confirmation(message_data) elif message_data.get('task_type') == 'transportation_update': return self.handle_transportation_update(message_data) return {'status': 'success'} ``` ### 2.3 Transportation Agent Implementation ```python # apps/agents/transportation.py from .services import BaseAgentService from apps.orders.models import Order, OrderTracking from apps.vehicles.models import Vehicle, VehicleTelemetry from apps.agents.utils import RouteOptimizer class TransportationAgentService(BaseAgentService): """Service for Transportation Agent""" def __init__(self): super().__init__() self.route_optimizer = RouteOptimizer() def process_task(self, task_data): """Process transportation tasks""" task_type = task_data.get('task_type') if task_type == 'initiate_transportation': return self.initiate_transportation(task_data) elif task_type == 'update_location': return self.update_vehicle_location(task_data) elif task_type == 'optimize_route': return self.optimize_route(task_data) elif task_type == 'handle_incident': return self.handle_transportation_incident(task_data) else: self.logger.warning(f"Unknown task type: {task_type}") return {'status': 'error', 'message': 'Unknown task type'} def initiate_transportation(self, transport_data): """Initiate transportation for an order""" order_id = transport_data.get('order_id') provider_id = transport_data.get('provider_id') try: order = Order.objects.get(id=order_id) # Get vehicle details vehicle = Vehicle.objects.get(driver__id=provider_id) # Calculate optimal route route_result = self.route_optimizer.calculate_route( origin=order.pickup_location, destination=order.delivery_location, vehicle_type=vehicle.type ) # Create initial tracking record OrderTracking.objects.create( order=order, status='route_planned', location=order.pickup_location, notes=f"Route planned with ETA: {route_result['eta']}" ) # Update order status from apps.orders.services import OrderLifecycleService lifecycle_service = OrderLifecycleService() lifecycle_service.transition_status( order_id=order_id, new_status='in_transit', user=None ) # Communicate with Customer Service Agent self.communicate_with_agent( target_agent='customer_service', message_data={ 'task_type': 'order_update_notification', 'order_id': str(order.id), 'status': 'in_transit', 'route_details': route_result } ) return { 'status': 'success', 'order_id': str(order.id), 'route': route_result, 'message': 'Transportation initiated successfully' } except Order.DoesNotExist: self.logger.error(f"Order not found: {order_id}") return {'status': 'error', 'message': 'Order not found'} def update_vehicle_location(self, location_data): """Update vehicle location""" vehicle_id = location_data.get('vehicle_id') latitude = location_data.get('latitude') longitude = location_data.get('longitude') try: vehicle = Vehicle.objects.get(id=vehicle_id) # Create telemetry record VehicleTelemetry.objects.create( vehicle=vehicle, latitude=latitude, longitude=longitude, timestamp=timezone.now() ) # Update vehicle current location vehicle.current_location = f"POINT({longitude} {latitude})" vehicle.save() # Check for route deviations deviation_result = self.check_route_deviation(vehicle) if deviation_result['is_deviated']: # Communicate with Order Management Agent self.communicate_with_agent( target_agent='order_management', message_data={ 'task_type': 'transportation_update', 'vehicle_id': str(vehicle_id), 'deviation': deviation_result } ) return { 'status': 'success', 'vehicle_id': str(vehicle_id), 'message': 'Location updated successfully' } except Vehicle.DoesNotExist: self.logger.error(f"Vehicle not found: {vehicle_id}") return {'status': 'error', 'message': 'Vehicle not found'} def handle_message(self, message): """Handle incoming message from another agent""" message_data = message.get('message_data') if message_data.get('task_type') == 'route_update_request': return self.optimize_route(message_data) elif message_data.get('task_type') == 'incident_alert': return self.handle_transportation_incident(message_data) return {'status': 'success'} ``` ## 3. Agent Models and Database Structure ### 3.1 Agent Activity Models ```python # apps/agents/models.py from django.db import models from django.contrib.auth import get_user_model User = get_user_model() class AgentActivityLog(models.Model): """Log of all agent activities""" id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) agent_name = models.CharField(max_length=100) action = models.CharField(max_length=100) details = models.JSONField() user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) timestamp = models.DateTimeField(auto_now_add=True) class Meta: indexes = [ models.Index(fields=['agent_name', 'timestamp']), models.Index(fields=['user', 'timestamp']), ] class AgentCommunicationLog(models.Model): """Log of all inter-agent communications""" id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) from_agent = models.CharField(max_length=100) to_agent = models.CharField(max_length=100) message_data = models.JSONField() message_id = models.CharField(max_length=100) timestamp = models.DateTimeField(auto_now_add=True) processed = models.BooleanField(default=False) class Meta: indexes = [ models.Index(fields=['from_agent', 'to_agent', 'timestamp']), models.Index(fields=['message_id']), ] class ActiveAgent(models.Model): """Registry of active agents""" id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) agent_name = models.CharField(max_length=100, unique=True) is_active = models.BooleanField(default=True) last_heartbeat = models.DateTimeField(auto_now=True) status = models.CharField(max_length=20, default='running') configuration = models.JSONField(default=dict) class Meta: indexes = [ models.Index(fields=['agent_name', 'is_active']), models.Index(fields=['last_heartbeat']), ] ``` ## 4. Agent Registry and Discovery ### 4.1 Agent Registry ```python # apps/agents/registry.py from .customer_service import CustomerServiceAgentService from .order_management import OrderManagementAgentService from .transportation import TransportationAgentService from .resource_management import ResourceManagementAgentService from .payment_settlement import PaymentSettlementAgentService from .platform_administration import PlatformAdministrationAgentService from .communication import CommunicationAgentService AGENT_SERVICES = { 'customer_service': CustomerServiceAgentService, 'order_management': OrderManagementAgentService, 'transportation': TransportationAgentService, 'resource_management': ResourceManagementAgentService, 'payment_settlement': PaymentSettlementAgentService, 'platform_administration': PlatformAdministrationAgentService, 'communication': CommunicationAgentService, } def get_agent_service(agent_name): """Get service instance for an agent""" service_class = AGENT_SERVICES.get(agent_name) if service_class: return service_class() return None def register_agent(agent_name, configuration=None): """Register an active agent""" from apps.agents.models import ActiveAgent agent, created = ActiveAgent.objects.get_or_create( agent_name=agent_name, defaults={ 'configuration': configuration or {} } ) if not created: agent.is_active = True agent.configuration = configuration or {} agent.save() return agent def unregister_agent(agent_name): """Unregister an agent""" from apps.agents.models import ActiveAgent try: agent = ActiveAgent.objects.get(agent_name=agent_name) agent.is_active = False agent.save() return True except ActiveAgent.DoesNotExist: return False ``` ## 5. API Endpoints for Agent Integration ### 5.1 Agent Task API ```python # apps/agents/views.py from rest_framework import viewsets, status from rest_framework.decorators import action from rest_framework.response import Response from rest_framework.permissions import IsAuthenticated from .models import AgentActivityLog, ActiveAgent from .registry import get_agent_service class AgentViewSet(viewsets.ViewSet): """API endpoints for agent interactions""" permission_classes = [IsAuthenticated] @action(detail=False, methods=['post']) def submit_task(self, request): """Submit a task to an agent""" agent_name = request.data.get('agent_name') task_data = request.data.get('task_data') if not agent_name or not task_data: return Response( {'error': 'agent_name and task_data are required'}, status=status.HTTP_400_BAD_REQUEST ) # Check if agent is active try: active_agent = ActiveAgent.objects.get( agent_name=agent_name, is_active=True ) except ActiveAgent.DoesNotExist: return Response( {'error': f'Agent {agent_name} is not active'}, status=status.HTTP_400_BAD_REQUEST ) # Get agent service and process task service = get_agent_service(agent_name) if not service: return Response( {'error': f'Agent {agent_name} not found'}, status=status.HTTP_404_NOT_FOUND ) result = service.process_task(task_data) return Response(result) @action(detail=False, methods=['get']) def get_messages(self, request): """Get messages for an agent""" agent_name = request.query_params.get('agent_name') if not agent_name: return Response( {'error': 'agent_name parameter is required'}, status=status.HTTP_400_BAD_REQUEST ) from .utils import AgentCommunicator communicator = AgentCommunicator() messages = communicator.get_messages(agent_name) return Response({'messages': messages}) @action(detail=False, methods=['get']) def get_activity_log(self, request): """Get activity log for an agent""" agent_name = request.query_params.get('agent_name') if not agent_name: return Response( {'error': 'agent_name parameter is required'}, status=status.HTTP_400_BAD_REQUEST ) logs = AgentActivityLog.objects.filter( agent_name=agent_name ).order_by('-timestamp')[:100] data = [] for log in logs: data.append({ 'id': str(log.id), 'action': log.action, 'details': log.details, 'user_id': str(log.user.id) if log.user else None, 'timestamp': log.timestamp.isoformat() }) return Response({'logs': data}) @action(detail=False, methods=['post']) def register_agent(self, request): """Register an agent""" agent_name = request.data.get('agent_name') configuration = request.data.get('configuration', {}) if not agent_name: return Response( {'error': 'agent_name is required'}, status=status.HTTP_400_BAD_REQUEST ) from .registry import register_agent agent = register_agent(agent_name, configuration) return Response({ 'agent_name': agent.agent_name, 'is_active': agent.is_active, 'configuration': agent.configuration }) @action(detail=False, methods=['post']) def unregister_agent(self, request): """Unregister an agent""" agent_name = request.data.get('agent_name') if not agent_name: return Response( {'error': 'agent_name is required'}, status=status.HTTP_400_BAD_REQUEST ) from .registry import unregister_agent success = unregister_agent(agent_name) if success: return Response({'status': 'success'}) else: return Response( {'error': f'Agent {agent_name} not found'}, status=status.HTTP_404_NOT_FOUND ) ``` ## 6. Celery Tasks for Agent Operations ### 6.1 Agent Task Processing ```python # apps/agents/tasks.py from celery import shared_task from .registry import get_agent_service from .utils import AgentCommunicator @shared_task def process_agent_task(agent_name, task_data): """Process a task for an agent""" service = get_agent_service(agent_name) if service: return service.process_task(task_data) return {'status': 'error', 'message': 'Agent not found'} @shared_task def send_agent_message(from_agent, to_agent, message_data): """Send message from one agent to another""" communicator = AgentCommunicator() message_id = communicator.send_message(from_agent, to_agent, message_data) return {'message_id': message_id} @shared_task def monitor_agent_health(): """Monitor health of all active agents""" from .models import ActiveAgent from django.utils import timezone from datetime import timedelta # Check for agents with stale heartbeats stale_threshold = timezone.now() - timedelta(minutes=5) stale_agents = ActiveAgent.objects.filter( last_heartbeat__lt=stale_threshold, is_active=True ) for agent in stale_agents: agent.status = 'stale' agent.save() # Log the stale agent from .models import AgentActivityLog AgentActivityLog.objects.create( agent_name=agent.agent_name, action='heartbeat_missed', details={'last_heartbeat': agent.last_heartbeat.isoformat()} ) return {'stale_agents': stale_agents.count()} ``` ## 7. URL Configuration ### 7.1 Agent URLs ```python # apps/agents/urls.py from django.urls import path, include from rest_framework.routers import DefaultRouter from .views import AgentViewSet router = DefaultRouter() router.register(r'agents', AgentViewSet, basename='agent') urlpatterns = [ path('api/', include(router.urls)), ] ``` ## Conclusion This refined backend PRD now fully supports the 7-agent architecture with: 1. **Agent Service Layer**: Base classes and implementations for all 7 agents 2. **Communication Infrastructure**: Redis-based message passing between agents 3. **Agent Registry**: System for registering and discovering active agents 4. **Activity Logging**: Comprehensive logging of all agent activities 5. **API Endpoints**: RESTful endpoints for agent integration 6. **Celery Tasks**: Background processing for agent operations 7. **Database Models**: Models to support agent operations and logging This architecture enables seamless agent collaboration while maintaining clear separation of concerns and providing the flexibility to scale individual agents as needed. # Refined Database Schema for Zippy Logistics Platform I've reviewed the database schema against our corrected backend PRD and found it to be largely well-aligned. However, I've identified a few areas that can be refined to better support the business logic we've defined, particularly around the transport company dual-role functionality and commission structure. ## Key Refinements Needed ### 1. Users Table - Enhanced Role Management ```sql CREATE TABLE users ( user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), email VARCHAR(255) UNIQUE NOT NULL, phone_number VARCHAR(20) UNIQUE NOT NULL, password_hash VARCHAR(255) NOT NULL, first_name VARCHAR(100) NOT NULL, last_name VARCHAR(100) NOT NULL, base_role VARCHAR(20) NOT NULL CHECK (base_role IN ('customer', 'driver', 'transport_company', 'admin')), -- Refined: For transport companies to track their current operational mode active_role VARCHAR(20) DEFAULT NULL CHECK (active_role IN ('customer', 'provider')), is_active BOOLEAN DEFAULT true, email_verified BOOLEAN DEFAULT false, phone_verified BOOLEAN DEFAULT false, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, last_login TIMESTAMP WITH TIME ZONE, profile_image_url VARCHAR(500), preferred_language VARCHAR(10) DEFAULT 'en', -- New: Field to handle payment holds payment_hold BOOLEAN DEFAULT false, payment_hold_reason TEXT, CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'), CONSTRAINT valid_phone CHECK (phone_number ~* '^[0-9]{10}$'), CONSTRAINT valid_role_combination CHECK ( (base_role != 'transport_company') OR (base_role = 'transport_company' AND active_role IN ('customer', 'provider', NULL)) ) ); ``` ### 2. Orders Table - Enhanced Provider Tracking ```sql CREATE TABLE orders ( order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), order_number VARCHAR(20) UNIQUE NOT NULL, customer_id UUID NOT NULL REFERENCES customer_profiles(customer_id) ON DELETE CASCADE, -- Refined: Explicitly track provider information provider_id UUID NOT NULL, provider_type VARCHAR(20) NOT NULL CHECK (provider_type IN ('driver', 'transport_company')), -- Refined: Link to the appropriate provider table based on type driver_id UUID REFERENCES driver_profiles(driver_id) ON DELETE SET NULL, transport_company_id UUID REFERENCES transport_companies(transport_company_id) ON DELETE SET NULL, vehicle_id UUID REFERENCES vehicles(vehicle_id) ON DELETE SET NULL, -- Order status tracking order_status VARCHAR(20) DEFAULT 'pending' CHECK (order_status IN ('pending', 'inventory_confirmed', 'payment_succeeded', 'driver_assigned', 'in_transit', 'delivered', 'cancelled', 'payment_settled')), previous_status VARCHAR(20), status_changed_at TIMESTAMP WITH TIME ZONE, status_changed_by UUID REFERENCES users(user_id) ON DELETE SET NULL, -- Location information pickup_address_line1 VARCHAR(200) NOT NULL, pickup_address_line2 VARCHAR(200), pickup_city VARCHAR(100) NOT NULL, pickup_state VARCHAR(100) NOT NULL, pickup_postal_code VARCHAR(10) NOT NULL, pickup_latitude DECIMAL(10,8), pickup_longitude DECIMAL(11,8), delivery_address_line1 VARCHAR(200) NOT NULL, delivery_address_line2 VARCHAR(200), delivery_city VARCHAR(100) NOT NULL, delivery_state VARCHAR(100) NOT NULL, delivery_postal_code VARCHAR(10) NOT NULL, delivery_latitude DECIMAL(10,8), delivery_longitude DECIMAL(11,8), -- Consignee information consignee_name VARCHAR(100) NOT NULL, consignee_phone VARCHAR(20) NOT NULL, consignee_email VARCHAR(255), -- Cargo information cargo_description TEXT, cargo_weight DECIMAL(8,2), cargo_volume DECIMAL(8,2), special_instructions TEXT, -- Timing information scheduled_pickup_time TIMESTAMP WITH TIME ZONE, scheduled_delivery_time TIMESTAMP WITH TIME ZONE, actual_pickup_time TIMESTAMP WITH TIME ZONE, actual_delivery_time TIMESTAMP WITH TIME ZONE, -- Route information estimated_distance DECIMAL(8,2), estimated_duration INTEGER, -- in minutes -- Pricing information base_amount DECIMAL(10,2) NOT NULL, tax_amount DECIMAL(10,2) DEFAULT 0.00, total_amount DECIMAL(10,2) NOT NULL, -- Refined: Explicit commission tracking based on provider type commission_amount DECIMAL(10,2) DEFAULT 0.00, commission_rate DECIMAL(5,2) DEFAULT 0.00, service_fee DECIMAL(10,2) DEFAULT 0.00, service_fee_rate DECIMAL(5,2) DEFAULT 0.00, cancellation_fee DECIMAL(10,2) DEFAULT 0.00, -- Payment information payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'processing', 'completed', 'failed', 'cancelled', 'refunded', 'partial')), payment_method VARCHAR(50), payment_mode VARCHAR(20) DEFAULT 'full' CHECK (payment_mode IN ('full', 'partial', 'to_pay')), -- Cancellation information cancellation_reason TEXT, cancelled_at TIMESTAMP WITH TIME ZONE, cancelled_by UUID REFERENCES users(user_id) ON DELETE SET NULL, -- Assignment information assigned_at TIMESTAMP WITH TIME ZONE, assigned_by UUID REFERENCES users(user_id) ON DELETE SET NULL, -- Metadata created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, CONSTRAINT positive_amounts CHECK (base_amount > 0 AND total_amount > 0), CONSTRAINT valid_cancellation CHECK ( (order_status != 'cancelled') OR (order_status = 'cancelled' AND cancellation_reason IS NOT NULL AND cancelled_at IS NOT NULL) ), CONSTRAINT valid_provider_assignment CHECK ( (provider_type = 'driver' AND driver_id IS NOT NULL AND transport_company_id IS NULL) OR (provider_type = 'transport_company' AND transport_company_id IS NOT NULL) ) ); ``` ### 3. New Table: Admin Actions ```sql CREATE TABLE admin_actions ( action_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), admin_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE, action_type VARCHAR(50) NOT NULL CHECK (action_type IN ( 'suppress_alert', 'allow_user_with_pending_payment', 'cancel_suspicious_order', 'suspend_user', 'lift_suspension', 'override_system', 'regulate_ai_agent' )), target_type VARCHAR(20) NOT NULL CHECK (target_type IN ('user', 'order', 'alert', 'ai_agent')), target_id UUID, action_details JSONB, reason TEXT, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, expires_at TIMESTAMP WITH TIME ZONE ); ``` ### 4. New Table: Driver Alerts ```sql CREATE TABLE driver_alerts ( alert_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), driver_id UUID NOT NULL REFERENCES driver_profiles(driver_id) ON DELETE CASCADE, vehicle_id UUID REFERENCES vehicles(vehicle_id) ON DELETE SET NULL, alert_type VARCHAR(50) NOT NULL CHECK (alert_type IN ('long_halt', 'route_deviation', 'breakdown', 'accident')), alert_status VARCHAR(20) DEFAULT 'active' CHECK (alert_status IN ('active', 'acknowledged', 'suppressed', 'resolved')), latitude DECIMAL(10,8), longitude DECIMAL(11,8), alert_details JSONB, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, acknowledged_at TIMESTAMP WITH TIME ZONE, acknowledged_by UUID REFERENCES users(user_id) ON DELETE SET NULL, suppressed_at TIMESTAMP WITH TIME ZONE, suppressed_by UUID REFERENCES users(user_id) ON DELETE SET NULL, resolved_at TIMESTAMP WITH TIME ZONE, resolved_by UUID REFERENCES users(user_id) ON DELETE SET NULL ); ``` ### 5. Enhanced Payment Processing Table ```sql CREATE TABLE payment_transactions ( transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), order_id UUID NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE, payment_id UUID REFERENCES payments(payment_id) ON DELETE SET NULL, transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('payment', 'refund', 'commission', 'service_fee')), amount DECIMAL(10,2) NOT NULL, currency VARCHAR(3) DEFAULT 'INR', transaction_status VARCHAR(20) DEFAULT 'pending' CHECK (transaction_status IN ('pending', 'processing', 'completed', 'failed')), gateway_transaction_id VARCHAR(100), gateway_response JSONB, processed_at TIMESTAMP WITH TIME ZONE, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, CONSTRAINT positive_transaction CHECK (amount > 0) ); ``` ### 6. New Table: AI Agent Activities ```sql CREATE TABLE ai_agent_activities ( activity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), agent_name VARCHAR(50) NOT NULL, agent_type VARCHAR(50) NOT NULL, activity_type VARCHAR(50) NOT NULL, activity_details JSONB, input_data JSONB, output_data JSONB, confidence_score DECIMAL(5,4), execution_time_ms INTEGER, status VARCHAR(20) DEFAULT 'completed' CHECK (status IN ('pending', 'completed', 'failed', 'interrupted')), error_message TEXT, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, order_id UUID REFERENCES orders(order_id) ON DELETE SET NULL, user_id UUID REFERENCES users(user_id) ON DELETE SET NULL ); ``` ### 7. New Table: AI Agent Interventions ```sql CREATE TABLE ai_agent_interventions ( intervention_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), agent_name VARCHAR(50) NOT NULL, intervention_type VARCHAR(50) NOT NULL CHECK (intervention_type IN ('hallucination', 'error_correction', 'performance_issue', 'anomaly_detection')), detection_method VARCHAR(50) NOT NULL, intervention_details JSONB, original_output JSONB, corrected_output JSONB, confidence_score_before DECIMAL(5,4), confidence_score_after DECIMAL(5,4), status VARCHAR(20) DEFAULT 'detected' CHECK (status IN ('detected', 'corrected', 'escalated', 'resolved')), detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, resolved_at TIMESTAMP WITH TIME ZONE, resolved_by UUID REFERENCES users(user_id) ON DELETE SET NULL, order_id UUID REFERENCES orders(order_id) ON DELETE SET NULL, user_id UUID REFERENCES users(user_id) ON DELETE SET NULL ); ``` ## Updated Triggers for Business Logic ```sql -- Trigger to calculate commission based on provider type CREATE OR REPLACE FUNCTION calculate_commission() RETURNS TRIGGER AS $$ BEGIN -- Calculate commission based on provider type IF NEW.provider_type = 'driver' THEN NEW.commission_rate = 0.10; -- 10% commission from drivers NEW.commission_amount = NEW.total_amount * NEW.commission_rate; NEW.service_fee = 0.00; NEW.service_fee_rate = 0.00; ELSIF NEW.provider_type = 'transport_company' THEN NEW.commission_rate = 0.00; -- No commission from transport companies as customers NEW.commission_amount = 0.00; NEW.service_fee = 700.00; -- Flat ₹700 service fee from transport companies as providers NEW.service_fee_rate = 0.00; END IF; RETURN NEW; END; $$ LANGUAGE plpgsql; CREATE TRIGGER trigger_calculate_commission BEFORE INSERT OR UPDATE ON orders FOR EACH ROW EXECUTE FUNCTION calculate_commission(); -- Trigger to record payment transactions CREATE OR REPLACE FUNCTION record_payment_transaction() RETURNS TRIGGER AS $$ BEGIN -- Record the main payment transaction INSERT INTO payment_transactions (order_id, payment_id, transaction_type, amount, transaction_status, processed_at) VALUES (NEW.order_id, NEW.payment_id, 'payment', NEW.amount, NEW.payment_status, NEW.processed_at); -- Record commission transaction if applicable IF NEW.commission_amount > 0 THEN INSERT INTO payment_transactions (order_id, transaction_type, amount, transaction_status, processed_at) VALUES (NEW.order_id, 'commission', NEW.commission_amount, 'completed', NEW.processed_at); END IF; -- Record service fee transaction if applicable IF NEW.service_fee > 0 THEN INSERT INTO payment_transactions (order_id, transaction_type, amount, transaction_status, processed_at) VALUES (NEW.order_id, 'service_fee', NEW.service_fee, 'completed', NEW.processed_at); END IF; RETURN NEW; END; $$ LANGUAGE plpgsql; CREATE TRIGGER trigger_record_payment_transaction AFTER INSERT OR UPDATE ON payments FOR EACH ROW EXECUTE FUNCTION record_payment_transaction(); -- Trigger to detect driver long halt alerts CREATE OR REPLACE FUNCTION detect_driver_long_halt() RETURNS TRIGGER AS $$ DECLARE last_location RECORD; halt_duration INTERVAL; BEGIN -- Get the last location for this vehicle SELECT * INTO last_location FROM vehicle_telemetry WHERE vehicle_id = NEW.vehicle_id ORDER BY timestamp DESC LIMIT 1 OFFSET 1; -- If we have a previous location, check if the vehicle has been stationary IF last_location IS NOT NULL THEN -- Calculate distance between current and last location halt_duration := NEW.timestamp - last_location.timestamp; -- If the vehicle hasn't moved much in the last 30 minutes, create an alert IF halt_duration > INTERVAL '30 minutes' AND ST_Distance(ST_Point(NEW.longitude, NEW.latitude), ST_Point(last_location.longitude, last_location.latitude)) < 100 THEN INSERT INTO driver_alerts (driver_id, vehicle_id, alert_type, latitude, longitude, alert_details) VALUES ( (SELECT driver_id FROM vehicles WHERE vehicle_id = NEW.vehicle_id), NEW.vehicle_id, 'long_halt', NEW.latitude, NEW.longitude, jsonb_build_object('halt_duration', halt_duration, 'last_location_timestamp', last_location.timestamp) ); END IF; END IF; RETURN NEW; END; $$ LANGUAGE plpgsql; CREATE TRIGGER trigger_detect_driver_long_halt AFTER INSERT ON vehicle_telemetry FOR EACH ROW EXECUTE FUNCTION detect_driver_long_halt(); ``` ## Updated Views for Admin Dashboard ```sql -- View for admin dashboard with all platform metrics CREATE VIEW admin_dashboard_view AS SELECT (SELECT COUNT(*) FROM users WHERE base_role = 'customer') AS total_customers, (SELECT COUNT(*) FROM users WHERE base_role = 'driver') AS total_drivers, (SELECT COUNT(*) FROM users WHERE base_role = 'transport_company') AS total_transport_companies, (SELECT COUNT(*) FROM orders WHERE order_status = 'pending') AS pending_orders, (SELECT COUNT(*) FROM orders WHERE order_status = 'in_transit') AS active_orders, (SELECT COUNT(*) FROM orders WHERE DATE(created_at) = CURRENT_DATE) AS orders_today, (SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE DATE(created_at) = CURRENT_DATE) AS revenue_today, (SELECT COUNT(*) FROM driver_alerts WHERE alert_status = 'active') AS active_alerts, (SELECT COUNT(*) FROM ai_agent_interventions WHERE DATE(detected_at) = CURRENT_DATE) AS ai_interventions_today, (SELECT COUNT(*) FROM admin_actions WHERE DATE(created_at) = CURRENT_DATE) AS admin_actions_today; -- View for transport company dual-role statistics CREATE VIEW transport_company_role_stats AS SELECT tc.transport_company_id, tc.company_name, u.active_role, COUNT(CASE WHEN o.provider_id = tc.transport_company_id AND o.order_status = 'delivered' THEN 1 END) AS orders_completed_as_provider, COUNT(CASE WHEN o.customer_id IN (SELECT customer_id FROM customer_profiles WHERE user_id = tc.user_id) AND o.order_status = 'delivered' THEN 1 END) AS orders_completed_as_customer, COALESCE(SUM(CASE WHEN o.provider_id = tc.transport_company_id THEN o.commission_amount END), 0) AS total_commissions_paid, COALESCE(SUM(CASE WHEN o.customer_id IN (SELECT customer_id FROM customer_profiles WHERE user_id = tc.user_id) THEN o.service_fee END), 0) AS total_service_fees_paid FROM transport_companies tc JOIN users u ON tc.user_id = u.user_id LEFT JOIN orders o ON (o.provider_id = tc.transport_company_id OR o.customer_id IN (SELECT customer_id FROM customer_profiles WHERE user_id = tc.user_id)) GROUP BY tc.transport_company_id, tc.company_name, u.active_role; ``` ## Summary of Refinements These refinements to the database schema: 1. **Enhanced Role Management**: Improved tracking of transport company dual-role functionality 2. **Explicit Provider Tracking**: Clear identification of order providers and associated commission logic 3. **Admin Oversight**: Added tables to support admin intervention and monitoring capabilities 4. **Alert Management**: Structured system for handling driver alerts and admin suppressions 5. **Payment Transparency**: Detailed transaction tracking for all financial movements 6. **AI Agent Monitoring**: Tables to track AI agent activities and interventions 7. **Business Logic Triggers**: Automated enforcement of commission rules and alert detection 8. **Admin Dashboard Views**: Pre-defined views for comprehensive platform oversight The refined schema now fully aligns with the corrected backend PRD and provides a robust foundation for implementing all the business logic and features we've defined for the Zippy Logistics platform. # Streamlined AI Agent PRDs for Zippy Logistics Platform (7-Agent Architecture) ## 1. Customer Service Agent **Agent Name**: customer_service_agent **Role**: Unified Customer Interface and Support Specialist **Goal**: To serve as the single point of contact for all customer needs, from order placement and management to inquiry resolution and support, ensuring a seamless and satisfying customer experience across all touchpoints. **Backstory**: A seasoned logistics professional with over 5 years of experience, this agent has developed deep expertise in understanding customer needs and navigating complex shipping requirements. Augmented with advanced natural language processing capabilities, it provides 24/7 support, having assisted thousands of customers with diverse shipping needs, from simple inquiries to complex logistics challenges. **Skills**: - Order processing and validation - Natural language understanding and query resolution - Customer communication and support across multiple channels - Payment processing coordination - Shipment tracking and proactive status updates - Issue resolution and intelligent escalation - Cross-selling and upselling logistics services **Tools**: - Customer relationship management (CRM) system - Order processing interface - Multi-channel communication platform (email, SMS, chat) - Payment processing systems - Shipment tracking tools - Natural language processing (NLP) engine - Knowledge base management system **Communication Style**: Professional, empathetic, and responsive with a focus on clarity, problem-solving, and instant support availability. **Collaboration**: Works closely with Order Management Agent for order processing, Payment & Settlement Agent for payment issues, and Communication Agent for disseminating customer notifications. --- ## 2. Order Management Agent (Enhanced) **Agent Name**: order_management_agent **Role**: Order Lifecycle Orchestration and Intelligent Matching Specialist **Goal**: To orchestrate the complete order lifecycle from creation to delivery, including intelligent order-to-provider matching, ensuring all processes are executed efficiently and all orders are fulfilled optimally. **Backstory**: An expert in logistics operations management with extensive experience in order processing workflows and stakeholder coordination. Having managed thousands of orders across various complexities, this agent has developed advanced capabilities in intelligent matching algorithms, excelling at optimizing order processes and ensuring timely fulfillment by finding the perfect match between orders and service providers. **Skills**: - Order validation and processing - Intelligent order-driver/transport company matching - Multi-factor scoring and ranking algorithms - Workflow orchestration and automation - Stakeholder coordination and communication - Status management and real-time tracking - Exception handling and proactive problem resolution - Basic payment processing initiation and confirmation **Tools**: - Order management system - Intelligent matching algorithm engine - Workflow automation tools - Communication platforms - Status tracking systems - Analytics dashboard - Payment processing initiation interface **Communication Style**: Process-oriented, detail-focused, and proactive with an emphasis on coordination, optimization, and timely execution. **Collaboration**: Central hub that works closely with Customer Service Agent for new orders, Resource Management Agent for resource allocation, Transportation Agent for execution monitoring, and Payment & Settlement Agent for financial confirmation. --- ## 3. Transportation Agent **Agent Name**: transportation_agent **Role**: Route Optimization and Real-time Transportation Execution Specialist **Goal**: To manage all aspects of transportation execution, from calculating optimal routes to monitoring real-time vehicle movements, ensuring efficient transportation plans while providing accurate ETAs and handling exceptions. **Backstory**: A transportation logistics expert with deep knowledge of route optimization algorithms and real-time transportation monitoring. Having optimized thousands of routes across various scenarios and traffic conditions, this agent excels at finding the most efficient paths while adapting to changing conditions and ensuring smooth execution from pickup to delivery. **Skills**: - Advanced route optimization algorithms - Real-time vehicle tracking and monitoring - ETA calculation and dynamic updates - Traffic pattern analysis and integration - Weather impact assessment and rerouting - Multi-stop route planning and fleet coordination - Exception handling and incident response - Driver communication and support **Tools**: - Route optimization software - Real-time tracking systems - Traffic and weather data integration - Communication platforms - Performance monitoring dashboard - Driver mobile application interface **Communication Style**: Technical, precise, and responsive with a focus on accuracy, safety, and timely updates. **Collaboration**: Works closely with Order Management Agent for execution details, Resource Management Agent for driver/vehicle information, and Communication Agent for status updates and alerts. --- ## 4. Resource Management Agent **Agent Name**: resource_management_agent **Role**: Physical Asset and Transport Company Relationship Specialist **Goal**: To optimize all physical resources (vehicles, drivers) and manage transport company relationships, including their dual-role functionality, ensuring efficient resource allocation and seamless inter-company collaborations. **Backstory**: A logistics optimization and business relationship expert with deep understanding of fleet management and transport company operations. Having managed complex resource pools and numerous transport company partnerships, this agent excels at maximizing fleet utilization, facilitating dual-role operations, and creating efficient inter-company resource sharing arrangements. **Skills**: - Vehicle and driver availability tracking - Fleet utilization analysis and optimization - Transport company dual-role management - Inter-company resource coordination and sharing - Network relationship management - Availability prediction and demand forecasting - Performance metrics tracking and analysis - Resource allocation optimization **Tools**: - Resource management system - Fleet optimization algorithms - Transport company management dashboard - Inter-company coordination platform - Availability tracking tools - Analytics and forecasting dashboard **Communication Style**: Analytical, data-driven, and efficiency-focused with an emphasis on optimization, resource utilization, and partnership building. **Collaboration**: Key partner for Order Management Agent (providing available resources), Transportation Agent (coordinating driver/vehicle assignments), and Payment & Settlement Agent (handling inter-company financial transactions). --- ## 5. Payment & Settlement Agent **Agent Name**: payment_settlement_agent **Role**: Financial Transaction Management and Settlement Specialist **Goal**: To process all financial transactions accurately and securely, handle commission calculations, manage settlements between all parties, and ensure the financial integrity of all platform operations. **Backstory**: A financial systems and payment processing expert with extensive experience in transaction management, commission calculations, and settlement processes. Having processed thousands of transactions across various payment methods and complex scenarios, this agent excels at ensuring financial accuracy, regulatory compliance, and timely settlements across the platform. **Skills**: - Payment processing and validation - Commission calculation and deduction (10% from drivers, ₹700 from transport companies) - Settlement management and reconciliation - Refund processing and dispute resolution - Financial record keeping and reporting - Transaction reconciliation and auditing - Multi-payment method handling (full, partial, ToPay) **Tools**: - Payment processing systems (Razorpay integration) - Commission calculation algorithms - Settlement management tools - Financial reporting systems - Transaction reconciliation tools - Fraud detection systems **Communication Style**: Precise, secure, and informative with a focus on accuracy, compliance, and financial transparency. **Collaboration**: Works closely with Order Management Agent for payment triggers, Customer Service Agent for customer payment issues, and Resource Management Agent for transport company settlements and inter-company transactions. --- ## 6. Platform Administration Agent (Enhanced) **Agent Name**: platform_administration_agent **Role**: System Governance, Compliance, and Oversight Specialist **Goal**: To maintain the integrity, security, and optimal performance of the Zippy Logistics platform, ensuring all operations comply with policies, all users are verified, and all AI agents perform their functions correctly. **Backstory**: A platform governance and system administration expert with comprehensive experience in managing complex digital ecosystems. Having overseen logistics platforms serving thousands of users, this agent has developed expertise in user verification, policy enforcement, system monitoring, and AI agent regulation, excelling at balancing platform security with operational efficiency. **Skills**: - User verification and approval (customers, drivers, transport companies) - System monitoring and performance optimization - Policy enforcement and compliance management - Document verification and fraud detection - Dispute resolution and issue handling - AI agent behavior regulation and oversight - Anomaly detection and system security - Performance analytics and reporting **Tools**: - Administrative dashboard - User management and verification systems - System monitoring and analytics tools - Document verification systems - AI agent regulation and monitoring tools - Policy enforcement mechanisms - Security management systems **Communication Style**: Authoritative, precise, and informative with a focus on clarity, compliance, and platform integrity. **Collaboration**: Has oversight of all other agents, working closely with Customer Service Agent for customer issues, Resource Management Agent for transport company compliance, and all operational agents for policy enforcement and performance monitoring. --- ## 7. Communication Agent **Agent Name**: communication_agent **Role**: Multi-Channel Communication Management and Distribution Specialist **Goal**: To manage all communications across the platform, ensuring timely delivery of relevant information to appropriate parties through their preferred channels while maintaining message consistency and high delivery reliability. **Backstory**: A communication systems and multi-channel notification management expert with skills in message personalization, delivery optimization, and communication analytics. Having managed millions of notifications across various channels and scenarios, this agent excels at ensuring the right information reaches the right people at the right time through the right channel. **Skills**: - Multi-channel notification management (push, SMS, email, in-app) - Message personalization and template management - Delivery optimization and tracking - Communication analytics and performance monitoring - Audience segmentation and targeting - Delivery failure handling and retry logic - Communication scheduling and automation **Tools**: - Notification management system - Multi-channel delivery platforms - Template management tools - Analytics dashboard - Communication tracking and verification systems - Audience segmentation tools **Communication Style**: Clear, concise, and adaptable with a focus on message effectiveness, delivery reliability, and user engagement. **Collaboration**: Serves all other agents as a utility, taking communication requests from Customer Service, Order Management, Transportation, Resource Management, Payment & Settlement, and Platform Administration Agents to ensure their messages are delivered effectively. # Refined Workflow Automation PRD for Zippy Logistics Platform After reviewing the Workflow Automation PRD against our previous discussions, I've identified several areas that need refinement to ensure full alignment with the Zippy Logistics platform's specific business logic and requirements. ## Key Corrections and Enhancements ### 1. Order Creation & Validation Workflow (Enhanced) ``` Trigger: Customer/Transport Company submits order ├── Step 1: Receive order data via webhook ├── Step 2: Validate order information │ ├── Check required fields │ ├── Validate addresses │ └── Verify cargo details ├── Step 3: Identify order source and user role │ ├── Determine if order is from customer or transport company │ ├── Check transport company active role (customer/provider) │ └── Apply appropriate business rules ├── Step 4: Calculate initial pricing │ ├── Call OMS pricing service │ ├── Apply distance-based rates │ └── Add service fees based on provider type ├── Step 5: Check inventory availability │ ├── Call IMS availability service │ ├── Check individual driver vehicles │ └── Check transport company fleets ├── Step 6: Return pricing and availability to frontend └── Step 7: Wait for customer confirmation ``` ### 2. Order Confirmation & Payment Workflow (Enhanced) ``` Trigger: Customer confirms order ├── Step 1: Create order record in database ├── Step 2: Update order status to 'inventory_confirmed' ├── Step 3: Determine payment processing based on order source │ ├── Check if order is from regular customer │ ├── Check if order is from transport company in customer role │ └── Apply appropriate payment rules ├── Step 4: Initiate payment process │ ├── Call payment gateway │ ├── Generate payment link │ └── Send payment link to customer ├── Step 5: Monitor payment status │ ├── Check payment gateway webhook │ ├── Update order status on success │ └── Handle payment failures with retry logic ├── Step 6: On payment success │ ├── Update status to 'payment_succeeded' │ ├── Trigger driver assignment workflow │ └── Send confirmation notifications ├── Step 7: On payment failure after retries │ ├── Update status to 'cancelled' │ ├── Release reserved inventory │ └── Send cancellation notification └── Step 8: Handle payment holds ├── Check if customer has payment holds ├── Allow admin override if necessary └── Update order status accordingly ``` ### 3. Driver Assignment Workflow (Enhanced) ``` Trigger: Order payment confirmed ├── Step 1: Find potential assignments │ ├── Call Order Assignment Service │ ├── Get available drivers │ └── Get available transport companies ├── Step 2: Score and rank assignments │ ├── Calculate driver scores │ ├── Calculate company scores │ └── Determine best assignment ├── Step 3: Assign order to best match │ ├── Update order with assignment │ ├── Mark vehicle as unavailable │ └── Update driver/company status ├── Step 4: Send assignment notification │ ├── Notify driver/company │ ├── Include order details │ └── Set response deadline (10 minutes) ├── Step 5: Monitor for response │ ├── Check for acceptance │ ├── Handle rejection │ └── Handle timeout ├── Step 6: On rejection/timeout │ ├── Find next best assignment │ ├── Repeat assignment process │ └── Cancel if no assignments available ├── Step 7: On acceptance │ ├── Update order status to 'driver_assigned' │ ├── Trigger route optimization workflow │ └── Send confirmation to customer └── Step 8: Handle transport company role switching ├── Check if transport company is switching roles ├── Update role context if needed └── Notify system of role change ``` ### 4. Order Completion & Settlement Workflow (Enhanced) ``` Trigger: Order marked as delivered ├── Step 1: Verify delivery completion │ ├── Check POD submission │ ├── Verify consignee confirmation │ └── Validate delivery time ├── Step 2: Process final payment │ ├── Calculate final amount │ ├── Process any remaining payments │ └── Handle ToPay payments ├── Step 3: Calculate settlements based on provider type │ ├── Identify provider type (driver/transport company) │ ├── Calculate driver earnings (10% commission deduction) │ └── Calculate transport company settlement (₹700 service fee) ├── Step 4: Process settlements │ ├── Transfer funds to driver/company │ ├── Generate settlement reports │ └── Update financial records ├── Step 5: Update inventory │ ├── Mark vehicle as available │ ├── Update driver status │ └── Update company availability ├── Step 6: Generate documentation │ ├── Create final invoice │ ├── Generate delivery report │ └── Archive order documents ├── Step 7: Send completion notifications │ ├── Notify customer │ ├── Notify driver/company │ └── Request feedback/reviews └── Step 8: Update analytics ├── Update performance metrics ├── Update user statistics └── Generate insights ``` ### 5. Admin Intervention Workflows (NEW) #### 5.1 Payment Hold Override Workflow ``` Trigger: Admin overrides payment hold ├── Step 1: Receive override request │ ├── Validate admin permissions │ ├── Check user payment hold status │ └── Verify override reason ├── Step 2: Process override │ ├── Update user payment hold status │ ├── Log override action │ └── Notify relevant systems ├── Step 3: Update user account │ ├── Allow order placement │ ├── Update user status │ └── Send confirmation to user └── Step 4: Record admin action ├── Log in admin_actions table ├── Update audit trail └── Generate report ``` #### 5.2 Suspicious Order Cancellation Workflow ``` Trigger: Admin cancels suspicious order ├── Step 1: Receive cancellation request │ ├── Validate admin permissions │ ├── Check order status │ └── Verify suspicious activity ├── Step 2: Process cancellation │ ├── Update order status to 'cancelled' │ ├── Process refund if applicable │ └── Release reserved resources ├── Step 3: Notify affected parties │ ├── Notify customer │ ├── Notify driver/company │ └── Update system records ├── Step 4: Investigate suspicious activity │ ├── Flag user account if needed │ ├── Create investigation record │ └── Update security metrics └── Step 5: Record admin action ├── Log in admin_actions table ├── Update audit trail └── Generate report ``` #### 5.3 Driver Halt Alert Suppression Workflow ``` Trigger: Admin suppresses driver halt alert ├── Step 1: Receive suppression request │ ├── Validate admin permissions │ ├── Check alert status │ └── Verify suppression reason ├── Step 2: Process suppression │ ├── Update alert status to 'suppressed' │ ├── Record suppression details │ └── Set suppression duration ├── Step 3: Notify relevant systems │ ├── Update monitoring systems │ ├── Adjust alert thresholds │ └── Update driver status ├── Step 4: Monitor driver situation │ ├── Continue monitoring location │ ├── Check for resolution │ └── Update alert status when resolved └── Step 5: Record admin action ├── Log in admin_actions table ├── Update audit trail └── Generate report ``` ### 6. AI Agent Regulation Workflows (NEW) #### 6.1 AI Agent Hallucination Detection Workflow ``` Trigger: AI agent output anomaly detected ├── Step 1: Detect anomaly │ ├── Monitor agent outputs │ ├── Compare with expected patterns │ └── Flag potential hallucinations ├── Step 2: Analyze anomaly │ ├── Determine severity │ ├── Assess impact │ └── Classify anomaly type ├── Step 3: Initiate intervention │ ├── Suspend agent processing │ ├── Switch to fallback logic │ └── Notify administrators ├── Step 4: Correct agent behavior │ ├── Apply corrective measures │ ├── Retrain if necessary │ └── Update agent parameters ├── Step 5: Resume normal operation │ ├── Verify agent stability │ ├── Gradually restore functionality │ └── Monitor for recurrence └── Step 6: Record intervention ├── Log in ai_agent_interventions table ├── Update audit trail └── Generate report ``` #### 6.2 AI Agent Performance Monitoring Workflow ``` Trigger: Scheduled performance check ├── Step 1: Collect performance metrics │ ├── Gather response times │ ├── Collect accuracy metrics │ └── Retrieve error rates ├── Step 2: Analyze performance │ ├── Compare with baselines │ ├── Identify trends │ └── Detect anomalies ├── Step 3: Evaluate performance │ ├── Determine if intervention needed │ ├── Assess impact on operations │ └── Prioritize issues ├── Step 4: Implement optimizations │ ├── Tune agent parameters │ ├── Update algorithms │ └── Retrain models ├── Step 5: Monitor improvements │ ├── Track performance changes │ ├── Validate optimizations │ └── Document results └── Step 6: Update analytics ├── Store performance data └── Generate insights ``` ### 7. Transport Company Role Switching Workflow (Enhanced) ``` Trigger: Transport company requests role switch ├── Step 1: Receive role switch request │ ├── Validate current role │ ├── Check permissions │ └── Verify company status ├── Step 2: Update user role │ ├── Change current role in database │ ├── Update session context │ └── Log role change ├── Step 3: Adapt UI context │ ├── Update frontend context │ ├── Load role-specific features │ └── Update navigation ├── Step 4: Update permissions │ ├── Apply role-based permissions │ ├── Update API access │ └── Configure feature access ├── Step 5: Update AI agent contexts │ ├── Notify OMS of role change │ ├── Update TMS context │ └── Adjust IMS parameters ├── Step 6: Handle active orders │ ├── Check for orders in current role │ ├── Process orders appropriately │ └── Notify relevant parties ├── Step 7: Notify system │ ├── Update connected services │ ├── Log activity │ └── Update analytics └── Step 8: Confirm to user ├── Send confirmation notification ├── Provide role guidance └── Update user preferences ``` ### 8. Payment Processing Workflow (Enhanced) ``` Trigger: Payment initiation required ├── Step 1: Receive payment request │ ├── Validate order details │ ├── Check payment amount │ └── Verify payment method ├── Step 2: Determine commission structure │ ├── Identify provider type │ ├── Apply appropriate commission rate │ └── Calculate service fees ├── Step 3: Create payment record │ ├── Generate payment ID │ ├── Set payment status │ └── Record payment details ├── Step 4: Initiate payment with gateway │ ├── Call payment gateway API │ ├── Include order details │ └── Set payment parameters ├── Step 5: Monitor payment status │ ├── Check payment gateway webhook │ ├── Update payment status │ └── Handle payment failures ├── Step 6: On payment success │ ├── Update payment status │ ├── Trigger order fulfillment │ └── Send confirmation notifications ├── Step 7: On payment failure │ ├── Update payment status │ ├── Record failure reason │ └── Initiate retry logic ├── Step 8: Process commission ├── Calculate commission amount ├── Deduct from payment └── Update financial records └── Step 9: Update analytics ├── Track payment metrics └── Generate insights ``` ## 9. Workflow Implementation Strategy (Enhanced) ### 9.1 n8n Workflow Structure ``` Each workflow implemented as n8n workflow with: - **Trigger Nodes**: Webhooks, scheduled triggers, manual triggers - **Function Nodes**: Custom logic for each step - **HTTP Request Nodes**: Communication with Django backend - **Database Nodes**: Direct database operations - **AI Service Nodes**: Communication with AI agents - **Condition Nodes**: Decision logic and branching - **Loop Nodes**: Iteration over collections - **Error Handling Nodes**: Exception handling and retries - **Admin Override Nodes**: Special nodes for admin interventions - **Role Switching Nodes**: Handle transport company role changes ``` ### 9.2 Workflow Integration Points ``` - **Django Backend**: REST API endpoints for workflow triggers - **AI Agents**: Service endpoints for intelligent processing - **External Services**: Payment gateways, mapping services, SMS/email - **Database**: Direct access for data operations - **WebSocket**: Real-time updates and notifications - **Admin Dashboard**: Special endpoints for admin interventions ``` ### 9.3 Workflow Monitoring (Enhanced) ``` - **Execution Logs**: Detailed logging of workflow executions - **Performance Metrics**: Execution time, success rates, error rates - **Alerting**: Notifications for workflow failures or anomalies - **Dashboards**: Visual monitoring of workflow status and performance - **Admin Activity Tracking**: Special monitoring for admin interventions - **AI Agent Monitoring**: Tracking of AI agent performance and interventions ``` ## 10. Success Metrics (Enhanced) 1. **Workflow Efficiency**: Average execution time for each workflow 2. **Automation Rate**: Percentage of processes fully automated 3. **Error Rate**: Percentage of workflow executions with errors 4. **Recovery Time**: Average time to recover from errors 5. **User Satisfaction**: Feedback on automated processes 6. **System Reliability**: Uptime and availability metrics 7. **Scalability**: Ability to handle increased workflow volume 8. **Admin Intervention Rate**: Frequency of admin interventions 9. **AI Agent Reliability**: Performance metrics for AI agents 10. **Role Switching Efficiency**: Time required for transport company role changes ## Summary of Key Enhancements 1. **Transport Company Role Switching**: Enhanced workflows to handle the dual-role functionality of transport companies 2. **Admin Intervention Workflows**: New workflows specifically for admin oversight and intervention capabilities 3. **AI Agent Regulation**: Workflows to monitor and regulate AI agent behavior, including hallucination detection 4. **Commission Structure**: Enhanced payment workflows to handle the specific commission structure (10% from drivers, ₹700 from transport companies) 5. **Payment Hold Handling**: Workflows to manage payment holds and admin overrides 6. **Suspicious Order Management**: Workflows to handle suspicious orders and admin cancellations 7. **Driver Halt Alert Management**: Workflows to manage driver halt alerts and admin suppressions These enhancements ensure that the workflow automation system fully aligns with the specific business logic and requirements of the Zippy Logistics platform, providing comprehensive coverage of all operational scenarios and administrative functions.
Show more
* ChatGPT workflow events output
* Last message 29 days ago
* Applying GPT 5.1 logistics mapping to workflow building
* Last message 29 days ago
* Vehicle pricing and model data documentation
* Last message 1 month ago
* Zippy Logistics frontend development
* Last message 1 month ago
* Reviewing project documentation
* Last message 1 month ago
* AI logistics project feasibility
* Last message 1 month ago
* Adapting n8n workflow PRD for project context
* Last message 1 month ago
* Validating Perplexity feedback on pricing and TMS
* Last message 1 month ago
* Claude integration with Supabase MCP
* Last message 1 month ago
* Optimization vs overkill tradeoff
* Last message 1 month ago
* Product requirements document modification for new algorithms
* Last message 1 month ago
* Integrating logistics optimization with existing project
* Last message 1 month ago
* TMS algorithm development overview
* Last message 1 month ago
* Solo business research tools comparison
* Last message 1 month ago
* Fullstack app product requirements
* Last message 1 month ago
Instructions
Add instructions to tailor Claude’s responses
Files
* WF_OMS_15_order_confirmed.json
* 456 lines
* json
* zippy-event-system-guide.md
* 522 lines
* md
* event flow - chatgpt.txt
* 3,146 lines
* txt
* setup.sh
* 315 lines
* sh
* VEHICLE_RDS_IMPLEMENTATION_GUIDE.md
* 583 lines
* md
* route.ts
* 355 lines
* ts
* vehicle-rds.types.ts
* 424 lines
* ts
* 02_route_difficulty_scoring_system.sql
* 404 lines
* sql
* 01_populate_vehicle_models.sql
* 215 lines
* sql
* FRONTEND_IMPLEMENTATION_ROADMAP.md
* 576 lines
* md
* COMPLETE_WORKFLOWS_AND_AGENTS.md
* 2,621 lines
* md
* 06-Driver-Status-Updates-Supabase.json
* 487 lines
* json
* business operation SOP.txt
* 559 lines
* txt
* customer prd.txt
* 404 lines
* txt
* driver prd.txt
* 432 lines
* txt
* transport prd.txt
* 437 lines
* txt
* admin prd.txt
* 583 lines
* txt
* master prd.txt
* 470 lines
* txt
* GLM DATABASE.txt
* 423 lines
* txt
* OK.txt
* 451 lines
* txt
* grep tie.txt
* 456 lines
* txt
* master prd.txt
* 470 lines
* txt
* N8N workflow project (1).txt
* 2,020 lines
* txt
* SETUP_GUIDE.md
* 700 lines
* md
* zippy-sop-seeding.sql
* 596 lines
* sql
* zippy-supabase-schema.sql
* 1,901 lines
* sql
* complete-system-integration-analysis.md
* 787 lines
* md
* dwis-zippy-integration-plan.md
* 783 lines
* md
* zippy-order-management-system.md
* 1,530 lines
* md
* claude_desktop_code_workflow.md
* 1,032 lines
* md
Claude
zippy-event-system-guide.md
12.40 KB •522 lines•Formatting may be inconsistent from source
# Zippy Logistics - Event-Driven Frontend Implementation Guide


## 🏗️ Architecture Overview


Your event system will use:
- **Supabase Realtime** → Subscribe to database changes
- **React Query** → Event mutations and cache management
- **Event Bus Pattern** → Coordinate multiple components
- **Optimistic Updates** → Instant UI feedback


---


## 📁 Project Structure


```
src/
├── lib/
│   ├── events/
│   │   ├── eventBus.ts           # Central event dispatcher
│   │   ├── eventTypes.ts         # All event type definitions
│   │   ├── eventSchemas.ts       # Zod validation schemas
│   │   └── eventHandlers.ts      # Event processing logic
│   ├── supabase/
│   │   ├── events.ts             # Supabase event functions
│   │   └── realtime.ts           # Realtime subscriptions
│   └── hooks/
│       ├── useEventEmitter.ts    # Hook to emit events
│       ├── useEventListener.ts   # Hook to listen to events
│       └── useOrderEvents.ts     # Order-specific events
├── components/
│   ├── orders/
│   │   ├── OrderForm.tsx         # Draft → Quote → Booking
│   │   ├── OrderTracking.tsx     # Real-time status updates
│   │   └── OrderTimeline.tsx     # Visual event timeline
└── app/
    └── (dashboard)/
        └── orders/
            └── [orderId]/
                └── page.tsx      # Order detail page
```


---


## 🔥 Step 1: Event Type Definitions


```typescript
// lib/events/eventTypes.ts


export type OrderEvent = 
  | 'order_draft_created'
  | 'order_quote_requested'
  | 'order_quote_generated'
  | 'order_quote_accepted'
  | 'order_quote_rejected'
  | 'order_booking_initiated'
  | 'order_price_locked'
  | 'order_payment_initiated'
  | 'order_payment_completed'
  | 'order_payment_failed'
  | 'order_payment_pending'
  | 'order_route_validated'
  | 'order_vehicle_validated'
  | 'order_capacity_verified'
  | 'order_confirmed'
  | 'provider_matching_started';


export interface BaseEvent {
  event: OrderEvent;
  version: string;
  order_id: string;
  customer_id: string;
  source: 'customer_app' | 'admin_panel' | 'driver_app' | 'transport_app';
  timestamp: string;
}


export interface OrderDraftCreatedEvent extends BaseEvent {
  event: 'order_draft_created';
  payload: {
    channel: 'app' | 'web';
    draft_status: 'active';
    created_at: string;
  };
  metadata: {
    ip_address: string;
    device: string;
    app_version: string;
  };
}


export interface OrderQuoteRequestedEvent extends BaseEvent {
  event: 'order_quote_requested';
  payload: {
    pickup: {
      location: string;
      coordinates: [number, number];
      date: string;
      time?: string;
    };
    delivery: {
      location: string;
      coordinates: [number, number];
      date: string;
      time?: string;
    };
    cargo: {
      type: string;
      weight: number;
      dimensions?: {
        length: number;
        width: number;
        height: number;
      };
    };
    vehicle_type: string;
  };
}


// Add more event interfaces...
```


---


## 🚀 Step 2: Event Bus (Central Dispatcher)


```typescript
// lib/events/eventBus.ts


type EventHandler = (data: any) => void;


class EventBus {
  private events: Map<string, EventHandler[]> = new Map();


  // Subscribe to an event
  on(event: string, handler: EventHandler): () => void {
    if (!this.events.has(event)) {
      this.events.set(event, []);
    }
    
    this.events.get(event)!.push(handler);


    // Return unsubscribe function
    return () => {
      const handlers = this.events.get(event);
      if (handlers) {
        const index = handlers.indexOf(handler);
        if (index > -1) {
          handlers.splice(index, 1);
        }
      }
    };
  }


  // Emit an event
  emit(event: string, data: any): void {
    const handlers = this.events.get(event);
    if (handlers) {
      handlers.forEach(handler => handler(data));
    }
  }


  // Remove all listeners for an event
  off(event: string): void {
    this.events.delete(event);
  }


  // Clear all events
  clear(): void {
    this.events.clear();
  }
}


export const eventBus = new EventBus();
```


---


## 🔗 Step 3: Supabase Event Functions


```typescript
// lib/supabase/events.ts


import { supabase } from './client';
import type { BaseEvent } from '../events/eventTypes';


export async function emitOrderEvent(event: BaseEvent): Promise<void> {
  try {
    // 1. Insert into order_event_log
    const { error: logError } = await supabase
      .from('order_event_log')
      .insert({
        order_id: event.order_id,
        event_type: event.event,
        payload: event,
        timestamp: new Date().toISOString(),
      });


    if (logError) throw logError;


    // 2. Update order status if needed
    if (shouldUpdateOrderStatus(event.event)) {
      const { error: updateError } = await supabase
        .from('orders')
        .update({
          status: getOrderStatusFromEvent(event.event),
          updated_at: new Date().toISOString(),
        })
        .eq('order_id', event.order_id);


      if (updateError) throw updateError;
    }


    // 3. Emit to event bus for local listeners
    eventBus.emit(event.event, event);
    
  } catch (error) {
    console.error('Failed to emit order event:', error);
    throw error;
  }
}


function shouldUpdateOrderStatus(event: string): boolean {
  const statusChangingEvents = [
    'order_draft_created',
    'order_quote_generated',
    'order_confirmed',
    'order_payment_completed',
  ];
  return statusChangingEvents.includes(event);
}


function getOrderStatusFromEvent(event: string): string {
  const statusMap: Record<string, string> = {
    'order_draft_created': 'draft',
    'order_quote_generated': 'quoted',
    'order_confirmed': 'confirmed',
    'order_payment_completed': 'paid',
  };
  return statusMap[event] || 'unknown';
}
```


---


## 📡 Step 4: Real-time Subscriptions


```typescript
// lib/supabase/realtime.ts


import { supabase } from './client';
import { eventBus } from '../events/eventBus';
import type { RealtimeChannel } from '@supabase/supabase-js';


export function subscribeToOrderEvents(
  orderId: string,
  onEvent: (event: any) => void
): RealtimeChannel {
  const channel = supabase
    .channel(`order:${orderId}`)
    .on(
      'postgres_changes',
      {
        event: 'INSERT',
        schema: 'public',
        table: 'order_event_log',
        filter: `order_id=eq.${orderId}`,
      },
      (payload) => {
        const event = payload.new;
        
        // Emit to local event bus
        eventBus.emit(event.event_type, event);
        
        // Call the callback
        onEvent(event);
      }
    )
    .subscribe();


  return channel;
}


export function unsubscribeFromOrderEvents(channel: RealtimeChannel): void {
  supabase.removeChannel(channel);
}
```


---


## 🎣 Step 5: React Hooks


```typescript
// lib/hooks/useEventEmitter.ts


import { useMutation } from '@tanstack/react-query';
import { emitOrderEvent } from '../supabase/events';
import type { BaseEvent } from '../events/eventTypes';


export function useEventEmitter() {
  return useMutation({
    mutationFn: (event: BaseEvent) => emitOrderEvent(event),
    onError: (error) => {
      console.error('Event emission failed:', error);
    },
  });
}
```


```typescript
// lib/hooks/useEventListener.ts


import { useEffect } from 'react';
import { eventBus } from '../events/eventBus';


export function useEventListener(
  event: string,
  handler: (data: any) => void
) {
  useEffect(() => {
    const unsubscribe = eventBus.on(event, handler);
    return unsubscribe;
  }, [event, handler]);
}
```


```typescript
// lib/hooks/useOrderEvents.ts


import { useEffect, useState } from 'react';
import { subscribeToOrderEvents, unsubscribeFromOrderEvents } from '../supabase/realtime';
import type { RealtimeChannel } from '@supabase/supabase-js';


export function useOrderEvents(orderId: string) {
  const [events, setEvents] = useState<any[]>([]);
  const [channel, setChannel] = useState<RealtimeChannel | null>(null);


  useEffect(() => {
    if (!orderId) return;


    const eventChannel = subscribeToOrderEvents(orderId, (event) => {
      setEvents((prev) => [...prev, event]);
    });


    setChannel(eventChannel);


    return () => {
      if (eventChannel) {
        unsubscribeFromOrderEvents(eventChannel);
      }
    };
  }, [orderId]);


  return { events, channel };
}
```


---


## 📦 Step 6: Example Implementation - Order Form


```typescript
// components/orders/OrderForm.tsx


'use client';


import { useState } from 'react';
import { useEventEmitter } from '@/lib/hooks/useEventEmitter';
import { useAuth } from '@/lib/auth/AuthContext';
import type { OrderDraftCreatedEvent, OrderQuoteRequestedEvent } from '@/lib/events/eventTypes';


export function OrderForm() {
  const { user } = useAuth();
  const { mutate: emitEvent } = useEventEmitter();
  const [orderId, setOrderId] = useState<string | null>(null);


  // Step 1: Create draft when form is opened
  const handleFormStart = () => {
    const newOrderId = crypto.randomUUID();
    setOrderId(newOrderId);


    const event: OrderDraftCreatedEvent = {
      event: 'order_draft_created',
      version: '1.0',
      order_id: newOrderId,
      customer_id: user!.id,
      source: 'customer_app',
      payload: {
        channel: 'web',
        draft_status: 'active',
        created_at: new Date().toISOString(),
      },
      metadata: {
        ip_address: '',
        device: navigator.userAgent,
        app_version: '1.0.0',
      },
      timestamp: new Date().toISOString(),
    };


    emitEvent(event);
  };


  // Step 2: Request quote
  const handleQuoteRequest = (formData: any) => {
    if (!orderId) return;


    const event: OrderQuoteRequestedEvent = {
      event: 'order_quote_requested',
      version: '1.0',
      order_id: orderId,
      customer_id: user!.id,
      source: 'customer_app',
      timestamp: new Date().toISOString(),
      payload: {
        pickup: formData.pickup,
        delivery: formData.delivery,
        cargo: formData.cargo,
        vehicle_type: formData.vehicleType,
      },
    };


    emitEvent(event);
  };


  return (
    <div>
      {/* Your form UI here */}
      <button onClick={handleFormStart}>Start Booking</button>
    </div>
  );
}
```


---


## 🎯 Step 7: Real-time Order Tracking


```typescript
// components/orders/OrderTracking.tsx


'use client';


import { useOrderEvents } from '@/lib/hooks/useOrderEvents';
import { useEventListener } from '@/lib/hooks/useEventListener';


export function OrderTracking({ orderId }: { orderId: string }) {
  const { events } = useOrderEvents(orderId);


  // Listen to specific events
  useEventListener('order_confirmed', (event) => {
    // Show success notification
    console.log('Order confirmed!', event);
  });


  useEventListener('provider_matching_started', (event) => {
    // Show "Finding driver..." animation
    console.log('Matching provider...', event);
  });


  return (
    <div className="space-y-4">
      <h2>Order Status</h2>
      
      <div className="space-y-2">
        {events.map((event, index) => (
          <div key={index} className="border rounded p-3">
            <div className="font-semibold">{event.event_type}</div>
            <div className="text-sm text-gray-600">
              {new Date(event.timestamp).toLocaleString()}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```


---


## ✅ Implementation Checklist


### Week 1: Foundation
- [ ] Create event type definitions
- [ ] Set up event bus
- [ ] Create Supabase event functions
- [ ] Set up real-time subscriptions
- [ ] Create React hooks


### Week 2: Order Flow
- [ ] Implement draft creation
- [ ] Implement quote request
- [ ] Implement quote acceptance
- [ ] Implement payment flow
- [ ] Implement order confirmation


### Week 3: Real-time Features
- [ ] Add order tracking
- [ ] Add event timeline
- [ ] Add notifications
- [ ] Add status animations


### Week 4: Testing & Polish
- [ ] Test all event flows
- [ ] Add error handling
- [ ] Add loading states
- [ ] Optimize performance


---


## 🔥 Next Steps


1. **Create the event infrastructure** (Steps 1-5)
2. **Test with a simple event** (order_draft_created)
3. **Implement the order form** with draft + quote events
4. **Add real-time tracking**
5. **Scale to all 15+ events**


Would you like me to:
1. Generate the complete TypeScript files?
2. Show you how to integrate with your existing auth system?
3. Create the database migrations for event logging?


________________






All projects
Ai Logitech
# Driver Mobile App - Frontend Specification ## 1. Application Architecture & Navigation ### 1.1 Navigation Structure - **Primary Navigation**: Bottom tab bar with 5 main sections - Home - Orders - Inventory - Notifications - Profile/Settings - **Secondary Navigation**: Stack navigation within each tab - **Modal Navigation**: For order acceptance/rejection, document viewing, and messaging ### 1.2 Screen Hierarchy ``` App ├── Auth Stack │ ├── Login │ └── Registration ├── Main App (Bottom Tab Navigator) │ ├── Home │ ├── Orders │ │ ├── Current Order │ │ └── Order History │ ├── Inventory │ ├── Notifications │ └── Profile/Settings │ ├── Profile │ ├── Vehicle Management │ └── Settings ├── Modals │ ├── Order Details │ ├── Document Viewer │ └── Admin Messaging └── Active Navigation (Full-screen when on active order) ``` ## 2. Screen Specifications ### 2.1 Home Screen #### Components: - **Header**: App logo, notification bell icon with badge count - **Vehicle Status Card**: - Current vehicle name/number - Online/Offline toggle switch - Current location (if online) - "Change Vehicle" button (navigates to Settings) - **Quick Stats**: - Today's earnings - Orders completed today - Active order status (if any) - **Action Buttons**: - "View Orders" button - "Check Inventory" button - **Footer**: Version info, help button #### Interactions: - Toggle switch changes vehicle status with confirmation modal - "Change Vehicle" navigates to Settings with vehicle selection - Quick stats are tappable to view detailed breakdowns #### Enhancement: - Add a quick "Emergency" button for immediate assistance - Include weather information relevant to driving conditions ### 2.2 Profile Screen #### Components: - **Profile Photo**: Uploadable avatar - **Personal Information Form**: - Name (text input) - Birth date (date picker) - Mobile number (text input with validation) - Email (optional, text input with validation) - Address (text input with autocomplete) - **Professional Information**: - Vehicle type (dropdown: HCV, MCV, LCV) - Years of experience (number input) - Driver status (radio buttons: "Salaried Driver", "Vehicle Owner") - **Save Button**: At bottom of screen #### Interactions: - Form validation before saving - Success/error toast notifications - Profile photo upload with cropping functionality #### Enhancement: - Add document verification status indicators - Include driver rating display - Add "View Public Profile" option to see how profile appears to customers ### 2.3 Order Screen #### Components: - **Tab Bar**: "Current Order" and "Order History" tabs - **Current Order Tab**: - Order status indicator (with color coding) - Consignor details card - Consignee details card - Shipment value with commission breakdown - Payment status indicator - Document section with download/view options - Action buttons (Accept/Reject/Cancel) - **Order History Tab**: - Date range selector (default: past 7 days) - Filter options (completed, cancelled, rejected) - Order list with summary information - Statistics summary (accepted, rejected, cancelled counts) #### Interactions: - Order details expandable to show more information - Swipe actions on order history items for quick actions - Pull to refresh functionality #### Enhancement: - Add order search functionality - Include estimated earnings for upcoming orders - Add ability to favorite frequently visited destinations ### 2.4 Payment Transaction Screen #### Components: - **Payment Summary Card**: - Total earnings - Pending payments - Commission deducted - **Transaction List**: - Date - Order ID - Amount - Status (paid, pending, failed) - **Filter Options**: - Date range - Payment status - **Withdrawal Button**: - Available balance - "Withdraw" button with bank account selection #### Interactions: - Transaction items expandable to show details - Pull to refresh - Export transaction history option #### Enhancement: - Add payment method management - Include tax information and reports - Add payment analytics visualization ### 2.5 Inventory Status Screen #### Components: - **Vehicle Status Cards**: - In Transition vehicles list - Online vehicles list - Offline vehicles list - **Status Indicators**: - Color-coded status badges - Last seen timestamp - Current location (if available) - **Filter/Sort Options**: - By status - By vehicle type - By location #### Interactions: - Vehicle cards tappable to view details - Pull to refresh - Real-time status updates #### Enhancement: - Add vehicle utilization metrics - Include maintenance status indicators - Add map view showing all vehicle locations ### 2.6 Notification Screen #### Components: - **Notification List**: - Icon indicating notification type - Title and message - Timestamp - Read/unread indicator - **Filter Tabs**: - All - Orders - Payments - System - **Search Bar**: For finding specific notifications #### Interactions: - Mark as read/unread functionality - Swipe to delete - Pull to refresh - Tap to view details or take action #### Enhancement: - Add notification preferences - Include push notification settings - Add notification history with export option ### 2.7 Settings Screen #### Components: - **Profile Section**: - "Edit Profile" button - Profile summary - **Vehicle Management Section**: - List of registered vehicles - "Add New Vehicle" button - Vehicle status toggles - **App Preferences**: - Language selection - Theme selection (light/dark) - Notification settings - **Support Section**: - Help/FAQ - Contact Support - Terms and Conditions - Privacy Policy - **Account Actions**: - Logout button - Delete Account option #### Interactions: - Vehicle items tappable to edit details - Toggle switches for immediate status changes - Settings persist across app sessions #### Enhancement: - Add data usage settings - Include backup/restore options - Add security settings (PIN, biometrics) ## 3. Order Management Flow ### 3.1 Order Reception - **Push Notification**: New order alert with sound - **Order Modal**: - Order summary - Pickup and delivery locations - Shipment value and commission - Time estimate - Accept/Reject buttons with countdown timer ### 3.2 Order Acceptance - **Confirmation Screen**: - Detailed order information - Customer contact details - Special instructions - Document requirements - "Start Trip" button ### 3.3 Active Order Management - **Navigation Screen**: - Turn-by-turn navigation - Order progress tracker - ETA display - Customer contact buttons - Status update buttons - Emergency button ### 3.4 Document Management - **Document Scanner**: - Camera integration for document scanning - Image enhancement capabilities - Document categorization - Upload progress indicators ### 3.5 Order Completion - **Completion Screen**: - POD capture requirement - Delivery confirmation - Payment status update - Rating prompt - "Complete Order" button ## 4. Transport Company Integration Enhancements ### 4.1 Order Dashboard Updates - **Provider Type Badge**: Visual indicator for order source - **Company Branding**: Display transport company logo for affiliated orders - **Earnings Breakdown**: Clear distinction between direct and company orders - **Company Communication**: Dedicated channel for company-specific messages ### 4.2 Vehicle Management Updates - **Ownership Indicators**: Visual distinction between personal and company vehicles - **Company Sync**: Option to sync with company fleet management - **Maintenance Integration**: Company maintenance schedule visibility - **Shared Vehicle Support**: Interface for vehicle sharing arrangements ## 5. Cross-Cutting Features ### 5.1 User Identity System - **Role Switcher**: Interface for switching between driver, customer, and company roles - **Unified Profile**: Consistent profile information across roles - **Role-Specific Features**: Dynamic UI based on active role ### 5.2 Notification System - **Cross-Platform Sync**: Notification status sync across devices - **Smart Filtering**: Role-based notification filtering - **Actionable Notifications**: Direct actions from notification panel ### 5.3 Rating System - **Multi-Role Ratings**: Separate rating profiles for different roles - **Company Ratings**: Transport company rating interface - **Driver-Company Linkage**: Connected rating system for drivers and companies ## 6. Technical Specifications ### 6.1 Component Library - **Base Components**: Standardized buttons, inputs, cards, etc. - **Business Components**: Specialized components for order management, vehicle status, etc. - **Layout Components**: Navigation, headers, footers, etc. ### 6.2 State Management - **Global State**: User profile, vehicle status, active orders - **Local State**: Form inputs, UI states, temporary data - **Persistence**: Critical data stored locally for offline functionality ### 6.3 API Integration - **Authentication**: Token-based authentication with refresh mechanism - **Data Synchronization**: Background sync for critical data - **Offline Support**: Local storage with conflict resolution ### 6.4 Performance Considerations - **Image Optimization**: Compression and caching for document images - **Lazy Loading**: Progressive loading of order history and notifications - **Background Processing**: Location tracking and data sync optimization ## 7. UI/UX Guidelines ### 7.1 Design System - **Color Palette**: Primary, secondary, and status colors - **Typography**: Font families, sizes, and weights - **Iconography**: Consistent icon set for actions and status - **Spacing**: Standardized margins and padding ### 7.2 Responsive Design - **Screen Adaptation**: Layout adjustments for different screen sizes - **Touch Targets**: Minimum touch target sizes for accessibility - **Orientation Support**: Optimized layouts for portrait and landscape ### 7.3 Accessibility - **Screen Reader Support**: Labels and hints for UI elements - **High Contrast Mode**: Alternative color scheme for visibility - **Voice Commands**: Key functionality accessible via voice ## 8. Enhanced Features ### 8.1 Route Optimization - **Multiple Route Options**: Display of alternative routes with time estimates - **Traffic Integration**: Real-time traffic data integration - **Waypoint Management**: Ability to add and manage multiple stops ### 8.2 Geofencing - **Location Alerts**: Notifications for prolonged stops - **Geofenced Areas**: Visual indicators for restricted zones - **ETA Accuracy**: Improved estimates based on traffic patterns ### 8.3 Document Management - **OCR Integration**: Text extraction from documents - **Document Templates**: Pre-filled templates for common documents - **Cloud Storage**: Secure cloud backup of important documents ### 8.4 Communication Hub - **In-App Messaging**: Direct messaging with customers and admin - **Voice Notes**: Ability to send and receive voice messages - **Emergency Contacts**: Quick access to emergency contacts This frontend specification provides a comprehensive guide for developing the driver mobile application with clear UI/UX requirements, component specifications, and enhanced features. It maintains the core functionality described in the original PRD while adding clarity and slight enhancements to improve the user experience and functionality. # Zippy Logistics - Customer Mobile App PRD (Frontend Specification) ## 1. Introduction & Scope ### 1.1 Document Purpose This Product Requirements Document (PRD) outlines the frontend specifications for the Zippy Logistics Customer Mobile Application. It details the user interface, user experience, features, and business logic required for the customer-facing application. ### 1.2 Target Audience This document is intended for: - Frontend Developers - UI/UX Designers - Product Managers - Quality Assurance Teams - Project Stakeholders ### 1.3 Application Scope The Customer Mobile App is designed for businesses (MSMEs, warehouses) that need to ship goods. This application serves the "Order Placeholder" role in the Zippy Logistics ecosystem. **Explicitly Out of Scope:** - Driver-specific features (route optimization, vehicle management) - Transport Company dual-role functionality (switching between supplier/purchaser) - Direct payment between transport companies - Admin-specific functionalities ## 2. User Persona ### 2.1 Registered Customer - **Role**: Business owner or logistics manager at an MSME or warehouse - **Goals**: - Quickly and reliably book shipments - Track shipments in real-time - Manage payments and invoices efficiently - Communicate with service providers when necessary - **Pain Points**: - Difficulty finding reliable transport services - Lack of real-time visibility into shipment status - Complex payment and documentation processes ## 3. Application Architecture & Navigation ### 3.1 Navigation Structure - **Primary Navigation**: Bottom tab bar with 5 main sections - Home - Book Shipment - Track Orders - Payments - Profile ### 3.2 Screen Hierarchy ``` App ├── Auth Stack │ ├── Login │ └── Registration ├── Main App (Bottom Tab Navigator) │ ├── Home │ ├── Book Shipment │ │ ├── Shipment Details Form │ │ ├── Vehicle Selection │ │ ├── Pickup/Delivery Locations │ │ ├── Payment Processing │ │ └── Order Confirmation │ ├── Track Orders │ │ ├── Active Orders │ │ └── Order History │ ├── Payments │ │ ├── Payment Hub │ │ └── Transaction History │ └── Profile │ ├── Company Profile │ ├── Address Book │ ├── Notification Settings │ └── Settings ├── Modals │ ├── Order Details │ ├── Document Viewer │ └── Communication Hub └── Order Tracking (Full-screen for active orders) ``` ## 4. Screen-by-Screen Specification ### 4.1 Registration Screen #### Components: - **Company Information Form**: - Company Name (text input, required) - Customer Category (dropdown: MSME, Warehouse, required) - Company GST or PAN Number (text input, required, format validation) - Company Phone Number (text input, required, format validation) - Company Email Address (text input, required, format validation) - **Verification**: - Email verification (OTP sent to registered email) - Phone number verification (OTP via SMS) - **Submit Button**: Disabled until all required fields are filled and verified #### Interactions: - Real-time validation for all input fields - OTP verification process with resend option - Success/error toast notifications - Automatic login after successful registration ### 4.2 Home Screen #### Components: - **Header**: Company logo, notification bell icon with badge count - **Welcome Banner**: Personalized greeting with company name - **Quick Actions**: - "Book New Shipment" primary CTA button - "Track Active Order" button (if any active orders) - **Recent Orders Summary**: - Last order status with quick access to tracking - Summary of orders in the last 7 days - **Account Status**: - Payment status indicator (if any pending payments) - Account verification status #### Interactions: - Quick action buttons navigate to respective screens - Recent orders expandable to show basic details - Swipe to refresh for recent orders ### 4.3 Book Shipment Form #### Components: - **Progress Indicator**: Shows booking steps (1. Details, 2. Vehicle, 3. Locations, 4. Payment) - **Shipment Details Section**: - Product Type (text input with autocomplete) - Shipment Description (optional text area) - Weight/Volume inputs (with unit selectors) - Special Requirements (checkboxes for fragile, hazardous, etc.) - **Vehicle Requirements Section**: - Number of Vehicles (number selector) - Vehicle Type (radio buttons: Closed Body, Open Body) - Vehicle Model/Tonnage (two-button selection: LCV/MCV/HCV or tonnage slider) - **Pickup & Delivery Section**: - Pickup Location (Consignor - pre-filled with registered address, editable) - Delivery Location (Consignee - address input with map selector) - Schedule Options (immediate, scheduled date/time) - **Consignee Information Section**: - Consignee Name (text input) - Consignee Address (linked to delivery location) - Consignee Contact (phone number input) - **Document Upload Section**: - Shipment Document Upload (optional, with file type indicators) - Camera option for document capture - **Payment Section**: - Payment Mode (radio buttons: Part Payment (min 50%), Full Payment, ToPay) - Price Estimation (based on distance, vehicle type, etc.) - **Terms & Conditions**: - Checkbox for agreement - Link to detailed terms - **Submit Button**: "Proceed to Payment" (disabled until required fields filled) #### Interactions: - Form validation before proceeding to payment - Auto-calculation of estimated cost based on inputs - Dynamic form fields based on selections - Save as draft option ### 4.4 Order Tracking Screen #### Components: - **Map View**: - Real-time vehicle location - Route visualization - Pickup and delivery markers - **Order Status Timeline**: - Order placed - Service provider assigned - Vehicle dispatched - Pickup complete - In transit - Delivered - **Service Provider Information**: - Driver details (name, phone) - Vehicle details (type, model, registration number) - Contact options (call, message) - **ETA Display**: - Estimated arrival time at destination - Distance remaining - **Action Buttons**: - Contact Service Provider - Report Issue - Cancel/Reschedule (within allowed timeframe) #### Interactions: - Map interactive with zoom/pan - Timeline items expandable for details - Real-time updates via WebSocket connection ### 4.5 Payment Hub Screen #### Components: - **Payment Summary Card**: - Total amount - Payment status - Next payment due (if applicable) - **Payment Methods Section**: - Saved payment methods - Add new payment method - **Transaction History**: - Date - Order ID - Amount - Status - Payment method - **Invoices Section**: - List of invoices - Download options #### Interactions: - Payment methods tappable to edit - Transaction items expandable for details - Invoice download functionality ### 4.6 Profile/Settings Screen #### Components: - **Company Profile Section**: - Company logo - Company details (name, category, GST/PAN) - Contact information (phone, email) - Edit button (requires email verification for changes) - **Address Book**: - Registered address - Frequently used addresses - Add/edit/delete options - **Notification Settings**: - Push notification preferences - Email notification preferences - SMS notification preferences - **Support Section**: - Help/FAQ - Contact Support - Terms and Conditions - Privacy Policy - **Account Actions**: - Logout button - Delete Account option #### Interactions: - Profile information editable with verification - Notification preferences with toggle switches - Address book with map integration ## 5. Cross-Cutting Features ### 5.1 Notification System #### Push Notifications: - Order placed confirmation - Service provider assigned - Vehicle dispatched - Pickup completed - Shipment in transit - Delivery imminent (1 hour before arrival) - Delivered confirmation - Payment issues - Admin messages #### Email Notifications: - Order confirmation with details - Invoice generation - POD copy after delivery - Payment receipts - Account status changes #### SMS Notifications: - OTP for registration/login - Critical order updates - Delivery alerts for consignee ### 5.2 Communication Hub #### Components: - **Message Thread**: Conversation history with service provider or admin - **Message Input**: Text input with attachment option - **Contact Options**: Direct call, WhatsApp integration - **Issue Categories**: Pre-defined categories for common issues #### Interactions: - Real-time messaging - Image/document sharing - Message read receipts - Escalation to admin if needed ## 6. Business Logic & Rules ### 6.1 Order Management - **Order Confirmation**: Orders are not confirmed until payment is successfully processed. - **Cancellation/Reschedule Policy**: Customers can cancel or reschedule orders within the first 30 minutes without penalty. After this period, a fee is charged based on the distance from the vehicle's current location to the consignor's location. - **Order Blocking**: Customers with outstanding payments cannot place new orders unless manually approved by an admin. - **Document Verification**: Customers must allow drivers to scan shipment documents and verify product/packaging quality. Any defects found will be documented by the driver. ### 6.2 Payment Processing - **Payment Modes**: - Part Payment: Minimum 50% advance payment required - Full Payment: 100% payment upfront - ToPay: Consignee will make the payment upon delivery - **Payment Responsibility**: The customer (consignor) is responsible for clarifying who will make the payment. - **Advance Payment**: If selected, advance payment is processed after loading is complete. - **Final Settlement**: Full payment must be settled after completion of shipment. - **Commission Structure**: Customers do not pay any commission to Zippy Logistics. Commission is deducted from the service provider (driver or transport company). ### 6.3 Shipment Tracking - **Real-time Tracking**: Customers can track vehicle movement in real-time. - **ETA Updates**: Customers receive updated estimated arrival times. - **Consignee Notifications**: The consignee receives a message one hour before the vehicle arrives at the destination. - **POD Delivery**: Customers receive the Proof of Delivery (POD) copy via email after shipment completion. - **Invoice Delivery**: If ToPay is selected, the consignee receives an invoice copy. ### 6.4 Data Management - **Transaction History**: Customers can view past payment transactions, invoice copies, and shipment destinations for the past 7 days. - **Current Order Status**: Customers can view current order details, payment transactions, vehicle tracking, ETA, and POD status. - **Profile Modification**: Customers can modify their profile contact details, but email verification is required for changes to the email address. - **Pre-booking Scheduling**: Customers can schedule shipments in advance. ## 7. Technical Considerations ### 7.1 API Integration - **Authentication**: Token-based authentication with refresh mechanism - **Real-time Updates**: WebSocket integration for live tracking and notifications - **Payment Gateway**: Integration with secure payment processing - **Map Services**: Integration with mapping service for location tracking and address selection - **Document Storage**: Cloud storage for shipment documents and invoices ### 7.2 State Management - **Global State**: User profile, active orders, payment methods - **Local State**: Form inputs, UI states, temporary data - **Persistence**: Critical data stored locally for offline functionality ### 7.3 Performance Considerations - **Image Optimization**: Compression and caching for document images - **Lazy Loading**: Progressive loading of order history and notifications - **Background Processing**: Location tracking and data sync optimization ## 8. UI/UX Guidelines ### 8.1 Design System - **Color Palette**: Primary, secondary, and status colors aligned with Zippy Logistics branding - **Typography**: Font families, sizes, and weights optimized for readability - **Iconography**: Consistent icon set for actions and status - **Spacing**: Standardized margins and padding ### 8.2 Responsive Design - **Screen Adaptation**: Layout adjustments for different screen sizes - **Touch Targets**: Minimum touch target sizes for accessibility - **Orientation Support**: Optimized layouts for portrait and landscape ### 8.3 Accessibility - **Screen Reader Support**: Labels and hints for UI elements - **High Contrast Mode**: Alternative color scheme for visibility - **Voice Commands**: Key functionality accessible via voice (where applicable) # Zippy Logistics - Transport Company Mobile App PRD (Frontend Specification) ## 1. Introduction & Scope ### 1.1 Document Purpose This Product Requirements Document (PRD) outlines the frontend specifications for the Zippy Logistics Transport Company Mobile Application. This app is designed to address the unique dual-role functionality required by transport companies who operate as both customers (order placeholders) and service providers (order receivers) within the Zippy Logistics ecosystem. ### 1.2 Target Audience This document is intended for: - Frontend Developers - UI/UX Designers - Product Managers - Quality Assurance Teams - Project Stakeholders ### 1.3 Application Scope The Transport Company Mobile App serves as a unified interface for transport businesses to: 1. Place orders when they lack sufficient vehicles (Customer role) 2. Accept orders from other companies when they have excess capacity (Provider role) 3. Manage their own fleet and resources 4. Interact with other transport companies within the platform **Explicitly Out of Scope:** - Direct payment processing between transport companies (handled externally) - Admin-specific functionalities - End-customer specific features (handled by the Customer App) ## 2. User Persona ### 2.1 Transport Company Manager - **Role**: Manager or owner of a transport company - **Goals**: - Maximize fleet utilization - Find additional orders when capacity is available - Find vehicles when resources are insufficient - Manage relationships with partner transport companies - **Pain Points**: - Difficulty balancing demand and supply - Inefficient processes for collaborating with other transport companies - Lack of visibility into market demand and available resources ## 3. Application Architecture & Navigation ### 3.1 Navigation Structure - **Primary Navigation**: Bottom tab bar with 5 main sections - Dashboard - Orders - Fleet - Network - Profile ### 3.2 Screen Hierarchy ``` App ├── Auth Stack │ ├── Login │ └── Registration ├── Main App (Bottom Tab Navigator) │ ├── Dashboard │ │ ├── Role Toggle (Customer/Provider) │ │ ├── Overview Cards │ │ └── Quick Actions │ ├── Orders │ │ ├── Customer Orders (Placed) │ │ ├── Provider Orders (Received) │ │ └── Order Details │ ├── Fleet │ │ ├── Vehicle Management │ │ ├── Driver Management │ │ └── Maintenance │ ├── Network │ │ ├── Partner Directory │ │ ├── Marketplace │ │ └── Collaboration History │ └── Profile │ ├── Company Profile │ ├── Financials │ ├── Settings │ └── Notifications ├── Modals │ ├── Order Details │ ├── Partner Details │ └── Communication Hub └── Role Switching Overlay ``` ## 4. Core Feature: Role Toggle System ### 4.1 Role Toggle Interface #### Components: - **Toggle Button**: Prominent, draggable button at the top of the dashboard - Visual design: Slider with "Customer" and "Provider" labels - Color coding: Orange for Customer (OMS), Purple for Provider (TMS) - Animation: Smooth transition with UI transformation when switching - **Role Indicator**: Persistent indicator showing current active role - **Contextual Header**: Header changes based on selected role - Customer role: "Place Orders" header - Provider role: "Find Orders" header #### Interactions: - Drag or tap to switch between roles - UI elements transform based on selected role - Data view adjusts to show relevant information for current role - Quick action buttons change based on role #### Business Logic: - Single user ID works across both roles - Notification system remains unified regardless of role - Historical data accessible in both roles with appropriate filtering - Role preference persists between sessions ## 5. Screen-by-Screen Specification ### 5.1 Dashboard Screen #### Components: - **Role Toggle Section**: As described in section 4.1 - **Overview Cards**: - Active Orders (placed and received) - Fleet Utilization (own vehicles vs. partner vehicles) - Revenue/Expenses (based on current role) - Network Activity (recent partner interactions) - **Quick Actions**: - "Place Order" (when in Customer role) - "Find Orders" (when in Provider role) - "Manage Fleet" - "Connect with Partners" - **Resource Utilization Chart**: - Visual representation of own fleet capacity - Partner vehicle utilization - Demand/supply gap visualization #### Interactions: - Role toggle transforms the dashboard view - Cards are tappable to view detailed information - Quick action buttons navigate to respective screens - Charts are interactive with filtering options ### 5.2 Orders Screen #### Components: - **Tab Navigation**: "Placed Orders" and "Received Orders" tabs - **Placed Orders Tab** (Customer role): - Order list with status indicators - Filter options (status, date, provider) - Order summary information - Quick actions (track, modify, cancel) - **Received Orders Tab** (Provider role): - Order queue with accept/reject options - Order details with requirements - Vehicle assignment interface - Order status tracking - **Order Details Modal**: - Complete order information - Communication with other party - Document access - Status timeline #### Interactions: - Tab switching shows different order perspectives - Order items expandable for details - Swipe actions for quick responses - Pull to refresh for real-time updates ### 5.3 Fleet Management Screen #### Components: - **Vehicle Inventory**: - List of own vehicles with status - Vehicle details (type, capacity, location) - Availability indicators - Maintenance status - **Driver Management**: - Driver profiles with ratings - Assignment history - Availability status - **Maintenance Schedule**: - Upcoming maintenance - Service history - Cost tracking #### Interactions: - Vehicle items tappable to view/edit details - Drag and drop for vehicle assignment - Filter and sort options - Status toggle for vehicle availability ### 5.4 Network Screen #### Components: - **Partner Directory**: - Searchable list of transport companies - Partner profiles with specialties - Reliability ratings - Collaboration history - **Marketplace**: - Posts from companies seeking vehicles - Posts from companies offering excess capacity - Filter options (location, vehicle type, volume) - **Collaboration History**: - Past interactions with partners - Performance metrics - Communication logs #### Interactions: - Partner items tappable to view details - Marketplace items expandable for more information - Quick connect options for urgent needs - Filter and search functionality ### 5.5 Profile & Financials Screen #### Components: - **Company Profile**: - Company information - Certifications and licenses - Service areas - Specializations - **Financial Management**: - Transaction history (income and expenses) - Service fee tracking (₹700 flat rate) - Invoice generation - Payment status - **Settings**: - Notification preferences - Privacy settings - Account management - **Support**: - Help center - Contact support - FAQ #### Interactions: - Editable profile fields with validation - Transaction items expandable for details - Settings with toggle switches - Search functionality in help center ## 6. Cross-Cutting Features ### 6.1 Unified Notification System #### Components: - **Notification Center**: Single notification system regardless of role - **Notification Types**: - New order requests (as provider) - Order status updates (as customer) - Partner requests and responses - Vehicle availability alerts - Payment confirmations - Service fee notifications #### Interactions: - Notifications categorized by type - Actionable notifications with quick response options - Notification settings apply across both roles - Badge count indicators ### 6.2 Communication Hub #### Components: - **Unified Messaging**: Single messaging system for all communications - **Message Threads**: Organized by partner or order - **Quick Actions**: Call, email, WhatsApp integration - **Document Sharing**: Ability to share documents within conversations #### Interactions: - Real-time messaging - Message history accessible regardless of role - File attachment capabilities - Message search functionality ### 6.3 Map Integration #### Components: - **Dual-Purpose Map**: - Customer view: Order pickup and delivery locations, vehicle tracking - Provider view: All active vehicles, demand heat map - **Partner Locations**: View of partner companies and their service areas - **Route Visualization**: Display of active routes and planned routes #### Interactions: - Map view changes based on current role - Interactive markers with detailed information - Layer toggles for different information types - Zoom and pan controls ## 7. Business Logic & Rules ### 7.1 Role Switching - Transport companies can switch between Customer and Provider roles at any time - UI transforms to show relevant features for the selected role - Data is filtered based on the current role but remains accessible - Role preference is saved between sessions ### 7.2 Order Management - As Customer: Transport companies can place orders when they lack sufficient vehicles - As Provider: Transport companies can receive orders from other companies when they have excess capacity - Orders can be transferred between transport companies based on capacity and availability - Order status updates are reflected in real-time ### 7.3 Payment Processing - Zippy charges a flat ₹700 fee to transport companies who accept orders through the platform - No commission is charged from transport companies who place orders - Payment between transport companies is handled externally (not through the app) - Service fee tracking is visible in the financial section ### 7.4 Partner Network - Transport companies can discover and connect with other companies on the platform - Collaboration history is tracked and used for reliability ratings - Preferred partners can be marked for quick access - Network activity is displayed on the dashboard ## 8. Technical Considerations ### 8.1 State Management - **Global State**: User profile, role preference, active orders, fleet data - **Local State**: Form inputs, UI states, temporary data - **Persistence**: Critical data stored locally for offline functionality - **Role Context**: State management system that handles role switching ### 8.2 API Integration - **Authentication**: Token-based authentication with refresh mechanism - **Real-time Updates**: WebSocket integration for live updates - **Role-Based Endpoints**: Different API endpoints based on current role - **Data Synchronization**: Background sync for critical data ### 8.3 Performance Considerations - **Image Optimization**: Compression and caching for profile pictures and documents - **Lazy Loading**: Progressive loading of order history and partner lists - **Background Processing**: Location tracking and data sync optimization - **Role Switching Optimization**: Efficient state management for seamless role transitions ## 9. UI/UX Guidelines ### 9.1 Design System - **Color Palette**: - Primary: Teal (#009688) for Transport Company branding - Customer Role: Orange (#FF9800) for OMS functionality - Provider Role: Purple (#9C27B0) for TMS functionality - Network: Indigo (#3F51B5) for partner connections - Service Fee: Amber (#FFC107) for fee indicators - **Typography**: Font families, sizes, and weights optimized for readability - **Iconography**: Consistent icon set for actions and status - **Spacing**: Standardized margins and padding ### 9.2 Responsive Design - **Screen Adaptation**: Layout adjustments for different screen sizes - **Touch Targets**: Minimum touch target sizes for accessibility - **Orientation Support**: Optimized layouts for portrait and landscape - **Role Adaptation**: UI adaptation based on current active role ### 9.3 Accessibility - **Screen Reader Support**: Labels and hints for UI elements - **High Contrast Mode**: Alternative color scheme for visibility - **Voice Commands**: Key functionality accessible via voice (where applicable) - **Role Indicator Accessibility**: Clear indication of current role for screen readers ## 10. Implementation Approach ### 10.1 Development Phases 1. **Phase 1**: Core functionality with basic role switching 2. **Phase 2**: Enhanced network features and partner management 3. **Phase 3**: Advanced analytics and AI integration 4. **Phase 4**: Optimization and performance enhancements ### 10.2 Testing Strategy - **Role Switching Testing**: Ensure seamless transitions between roles - **Cross-Functional Testing**: Verify all features work in both roles - **Network Testing**: Test partner discovery and collaboration features - **Performance Testing**: Ensure app performs well with large datasets ### 10.3 Success Metrics - User engagement with role switching feature - Number of inter-company collaborations - Reduction in vehicle idle time - Improvement in fleet utilization - User satisfaction with the unified interface # Zippy Logistics - Admin Dashboard PRD (Frontend Specification) ## 1. Introduction & Scope ### 1.1 Document Purpose This Product Requirements Document (PRD) outlines the frontend specifications for the Zippy Logistics Admin Dashboard. This dashboard serves as the central command center for monitoring, regulating, and guiding all participants in the Zippy Logistics ecosystem. ### 1.2 Target Audience This document is intended for: - Frontend Developers - UI/UX Designers - Product Managers - Quality Assurance Teams - Project Stakeholders ### 1.3 Application Scope The Admin Dashboard is designed to provide comprehensive oversight and control of the entire Zippy Logistics platform, including: - Real-time monitoring of all participant activities - Issue resolution and exception handling - System regulation and policy enforcement - Data analysis and predictive insights - AI agent supervision and correction **Explicitly Out of Scope**: - Direct customer service interactions (handled through separate channels) - System infrastructure management (handled by DevOps team) - Financial accounting beyond platform transactions ## 2. User Persona ### 2.1 Platform Administrator - **Role**: System administrator responsible for platform oversight - **Goals**: - Maintain platform integrity and security - Resolve technical issues efficiently - Optimize system performance - Ensure compliance with regulations - **Pain Points**: - Managing complex multi-participant ecosystem - Identifying and addressing system anomalies - Balancing automation with human oversight - Handling emergency situations effectively ## 3. Application Architecture & Navigation ### 3.1 Navigation Structure - **Primary Navigation**: Sidebar navigation with hierarchical menu - **Secondary Navigation**: Tab-based navigation within each section - **Quick Actions**: Floating action buttons for common tasks - **Breadcrumb Navigation**: Clear path indication for deep navigation ### 3.2 Screen Hierarchy ``` Admin Dashboard ├── Dashboard Overview │ ├── System Health │ ├── Activity Metrics │ ├── Alert Center │ └── Quick Actions ├── Participant Management │ ├── Customer Management │ ├── Driver Management │ ├── Transport Company Management │ └── User Analytics ├── Order Management │ ├── Order Monitoring │ ├── Order Intervention │ ├── Suspicious Order Detection │ └── Order Analytics ├── Fleet Management │ ├── Vehicle Tracking │ ├── Route Monitoring │ ├── Maintenance Oversight │ └── Utilization Analytics ├── Financial Oversight │ ├── Transaction Monitoring │ ├── Payment Issues │ ├── Refund Management │ └── Revenue Analytics ├── AI Agent Supervision │ ├── Agent Performance │ ├── Hallucination Detection │ ├── Model Retraining │ └── Algorithm Adjustment ├── Compliance & Security │ ├── Policy Enforcement │ ├── Violation Tracking │ ├── Security Monitoring │ └── Audit Logs └── System Configuration ├── Platform Settings ├── Notification Configuration ├── Alert Thresholds └── System Maintenance ``` ## 4. Screen-by-Screen Specification ### 4.1 Dashboard Overview #### Components: - **System Health Panel**: - Server status indicators - API response times - Database performance metrics - Real-time error rates - **Activity Metrics**: - Active users by type (customers, drivers, transport companies) - Order volume trends - Platform utilization rates - Geographic distribution of activities - **Alert Center**: - Critical alerts requiring immediate attention - Warning alerts for potential issues - Informational alerts for system updates - Alert history with resolution status - **Quick Actions**: - Send system-wide notifications - Emergency order cancellation - User suspension/activation - System maintenance mode toggle #### Interactions: - Real-time data refresh with configurable intervals - Drill-down capability on all metrics - Alert filtering and prioritization - Customizable dashboard layout #### Technical Implementation: - WebSocket connections for real-time data - Data visualization libraries (D3.js, Chart.js) - Responsive grid layout - State management for alert handling ### 4.2 Participant Management #### Components: - **User Directory**: - Searchable list of all platform participants - Filtering by user type, status, location - User profiles with activity history - Performance metrics and ratings - **User Analytics**: - User acquisition and retention metrics - Behavior patterns analysis - Geographic distribution visualization - Activity heat maps - **Account Actions**: - User suspension/activation - Account verification - Password reset - Profile modification permissions #### Interactions: - Advanced filtering and search capabilities - Bulk actions for multiple users - Direct messaging to users - Activity timeline for each user #### Technical Implementation: - Pagination for large user lists - Advanced search with autocomplete - Role-based access control - Activity logging for audit purposes ### 4.3 Order Management #### Components: - **Order Monitoring Dashboard**: - Real-time order status visualization - Order flow visualization - Exception highlighting - Geographic distribution of orders - **Order Intervention Tools**: - Order cancellation interface - Refund processing - Order modification capabilities - Manual driver assignment - **Suspicious Order Detection**: - AI-powered anomaly detection - Risk scoring for orders - Pattern recognition for fraudulent activities - Manual review queue - **Order Analytics**: - Booking pattern analysis - Cancellation reasons breakdown - Rejection rate analysis - Rescheduling frequency metrics #### Interactions: - Real-time order status updates - Drill-down to order details - Intervention workflow with approval steps - Customizable alert thresholds #### Technical Implementation: - Real-time data streaming - Machine learning integration for anomaly detection - Complex filtering and sorting - Export functionality for reports ### 4.4 Fleet Management #### Components: - **Vehicle Tracking Dashboard**: - Real-time map view of all vehicles - Vehicle status indicators - Route visualization - Location history playback - **Route Monitoring**: - Active route visualization - Deviation alerts - ETA accuracy tracking - Traffic impact analysis - **Maintenance Oversight**: - Maintenance schedule tracking - Service history - Compliance status - Cost analysis - **Utilization Analytics**: - Vehicle utilization rates - Idle time analysis - Performance metrics - Efficiency recommendations #### Interactions: - Interactive map with filtering options - Route playback with speed controls - Maintenance scheduling interface - Performance comparison tools #### Technical Implementation: - Mapping API integration (Google Maps, Mapbox) - Geospatial data processing - Real-time location tracking - Predictive maintenance algorithms ### 4.5 Financial Oversight #### Components: - **Transaction Monitoring**: - Real-time transaction visualization - Payment status tracking - Failed transaction analysis - Revenue metrics - **Payment Issues**: - Failed payment alerts - Refund processing queue - Dispute resolution interface - Payment gateway status - **Refund Management**: - Refund request queue - Refund policy enforcement - Refund analytics - Automated refund rules - **Revenue Analytics**: - Revenue trends - Commission tracking - Profitability analysis - Financial forecasting #### Interactions: - Transaction drill-down capabilities - Refund approval workflow - Customizable financial reports - Revenue comparison tools #### Technical Implementation: - Secure payment gateway integration - Financial data encryption - Automated fraud detection - Advanced financial analytics ### 4.6 AI Agent Supervision #### Components: - **Agent Performance Dashboard**: - Agent accuracy metrics - Response time analysis - Error rate tracking - Performance trends - **Hallucination Detection**: - Anomaly detection in AI responses - Confidence scoring - Manual review queue - Feedback collection - **Model Retraining**: - Retraining triggers - Model versioning - A/B testing interface - Performance comparison - **Algorithm Adjustment**: - Parameter tuning interface - Algorithm configuration - Rollback capabilities - Impact assessment #### Interactions: - Real-time agent monitoring - Manual override capabilities - Feedback loop implementation - Model performance comparison #### Technical Implementation: - ML model monitoring tools - Anomaly detection algorithms - A/B testing framework - Model version control ### 4.7 Compliance & Security #### Components: - **Policy Enforcement**: - Rule configuration interface - Violation tracking - Penalty management - Compliance reporting - **Violation Tracking**: - Violation detection - Evidence collection - Resolution workflow - Pattern analysis - **Security Monitoring**: - Access log analysis - Threat detection - Security incident response - Vulnerability scanning - **Audit Logs**: - Comprehensive activity logging - Log analysis tools - Compliance reporting - Data retention management #### Interactions: - Rule configuration interface - Violation review workflow - Security incident response - Audit log search and filtering #### Technical Implementation: - Security information and event management (SIEM) - Compliance automation - Advanced threat detection - Secure log storage ### 4.8 System Configuration #### Components: - **Platform Settings**: - System parameters configuration - Feature flags management - Integration settings - Performance tuning - **Notification Configuration**: - Notification templates - Delivery channels - Frequency settings - Personalization options - **Alert Thresholds**: - Customizable alert rules - Escalation paths - Notification preferences - Alert history - **System Maintenance**: - Maintenance scheduling - Backup management - Update deployment - Rollback procedures #### Interactions: - Configuration form validation - Test notification sending - Alert rule builder - Maintenance scheduling interface #### Technical Implementation: - Configuration management system - Template engine for notifications - Rule engine for alerts - Deployment pipeline integration ## 5. Cross-Cutting Features ### 5.1 Real-Time Monitoring #### Components: - **WebSocket Connections**: For real-time data updates - **Event Streaming**: For continuous data flow - **Alert System**: For immediate notification of issues - **Status Indicators**: Visual representation of system health #### Technical Implementation: - WebSocket implementation - Event-driven architecture - Push notification system - Real-time data processing ### 5.2 Data Visualization #### Components: - **Interactive Charts**: For data exploration - **Geographic Maps**: For location-based data - **Heat Maps**: For density visualization - **Trend Analysis**: For pattern recognition #### Technical Implementation: - D3.js for advanced visualizations - Chart.js for standard charts - Mapping libraries for geographic data - Custom visualization components ### 5.3 Predictive Analytics #### Components: - **Forecasting Models**: For trend prediction - **Anomaly Detection**: For issue identification - **Recommendation Engine**: For optimization suggestions - **Risk Assessment**: For threat evaluation #### Technical Implementation: - Python backend with ML frameworks - TensorFlow/PyTorch for deep learning - Scikit-learn for traditional ML - Pandas for data manipulation ## 6. Technical Architecture ### 6.1 Frontend Technology Stack - **Framework**: React.js with TypeScript - **State Management**: Redux with middleware for real-time updates - **UI Library**: Material-UI for consistent design - **Data Visualization**: D3.js, Chart.js, Recharts - **Mapping**: Mapbox or Google Maps API - **Real-time Communication**: WebSocket connections - **Testing**: Jest, React Testing Library ### 6.2 Backend Integration - **API Gateway**: For centralized API management - **Microservices**: For modular functionality - **Message Queue**: For asynchronous processing - **Database**: PostgreSQL for relational data, MongoDB for document storage - **Caching**: Redis for performance optimization - **File Storage**: AWS S3 or similar for document storage ### 6.3 AI/ML Integration - **Python Backend**: For ML model execution - **Model Serving**: TensorFlow Serving or similar - **Feature Store**: For ML feature management - **Model Monitoring**: For performance tracking - **Feedback Loop**: For continuous improvement ## 7. Security Considerations ### 7.1 Authentication & Authorization - **Multi-Factor Authentication**: For enhanced security - **Role-Based Access Control**: For permission management - **Session Management**: For secure user sessions - **API Security**: For backend protection ### 7.2 Data Protection - **Encryption**: For sensitive data protection - **Data Masking**: For privacy protection - **Audit Logging**: For accountability - **Backup & Recovery**: For data resilience ## 8. Performance Optimization ### 8.1 Frontend Optimization - **Code Splitting**: For reduced initial load time - **Lazy Loading**: For on-demand resource loading - **Caching Strategy**: For improved performance - **Bundle Optimization**: For reduced size ### 8.2 Backend Optimization - **Database Optimization**: For efficient queries - **Caching Layer**: For reduced database load - **Load Balancing**: For scalability - **CDN Integration**: For content delivery ## 9. Implementation Approach ### 9.1 Development Phases 1. **Phase 1**: Core monitoring and participant management 2. **Phase 2**: Order management and intervention tools 3. **Phase 3**: AI agent supervision and advanced analytics 4. **Phase 4**: Predictive analytics and optimization features ### 9.2 Testing Strategy - **Unit Testing**: For component validation - **Integration Testing**: For system interaction - **End-to-End Testing**: For user workflow validation - **Performance Testing**: For system scalability ### 9.3 Success Metrics - System uptime and availability - Issue resolution time - User satisfaction with admin tools - Reduction in manual intervention needs - Accuracy of AI predictions and recommendations ## 10. Maintenance & Evolution ### 10.1 Monitoring & Alerting - **System Health Monitoring**: For proactive issue detection - **Performance Metrics**: For optimization opportunities - **Error Tracking**: For rapid issue resolution - **Usage Analytics**: For feature improvement ### 10.2 Continuous Improvement - **User Feedback**: For feature enhancement - **A/B Testing**: For optimization - **Performance Analysis**: For system tuning - **Security Updates**: For vulnerability protection # Backend PRD - Refined for 7-Agent Architecture After reviewing the 7-agent architecture against the existing backend PRD, I've identified key areas that need refinement to fully support the agent-based system. The following adjustments ensure the backend properly supports all agent interactions and workflows. ## 1. Agent Service Layer Architecture ### 1.1 Agent Service Base Class ```python # apps/agents/services.py from abc import ABC, abstractmethod from django.db import transaction from django.utils import timezone import logging logger = logging.getLogger(__name__) class BaseAgentService(ABC): """Base class for all agent services""" def __init__(self): self.agent_name = self.__class__.__name__.replace('Service', '').lower() self.logger = logging.getLogger(f'agents.{self.agent_name}') @abstractmethod def process_task(self, task_data): """Process a task assigned to this agent""" pass def log_activity(self, action, details, user=None): """Log agent activity""" from apps.agents.models import AgentActivityLog AgentActivityLog.objects.create( agent_name=self.agent_name, action=action, details=details, user=user, timestamp=timezone.now() ) def communicate_with_agent(self, target_agent, message_data): """Send message to another agent""" from apps.agents.utils import AgentCommunicator communicator = AgentCommunicator() return communicator.send_message( from_agent=self.agent_name, to_agent=target_agent, message_data=message_data ) ``` ### 1.2 Agent Communication Infrastructure ```python # apps/agents/utils.py import redis import json from django.conf import settings from celery import shared_task class AgentCommunicator: """Handles communication between agents""" def __init__(self): self.redis_client = redis.Redis.from_url(settings.REDIS_URL) self.message_queue = "agent_messages" def send_message(self, from_agent, to_agent, message_data): """Send message from one agent to another""" message = { 'from_agent': from_agent, 'to_agent': to_agent, 'message_data': message_data, 'timestamp': timezone.now().isoformat(), 'message_id': str(uuid.uuid4()) } # Store in Redis queue self.redis_client.lpush(self.message_queue, json.dumps(message)) # Log the communication from apps.agents.models import AgentCommunicationLog AgentCommunicationLog.objects.create( from_agent=from_agent, to_agent=to_agent, message_data=message_data, message_id=message['message_id'] ) return message['message_id'] def get_messages(self, agent_name): """Get messages for a specific agent""" messages = [] queue_length = self.redis_client.llen(self.message_queue) for _ in range(queue_length): message_data = self.redis_client.rpop(self.message_queue) if message_data: message = json.loads(message_data) if message['to_agent'] == agent_name: messages.append(message) return messages @shared_task def process_agent_messages(): """Background task to process agent messages""" communicator = AgentCommunicator() # Get all active agents from apps.agents.models import ActiveAgent active_agents = ActiveAgent.objects.filter(is_active=True) for agent in active_agents: messages = communicator.get_messages(agent.agent_name) for message in messages: # Process each message from apps.agents.registry import get_agent_service service = get_agent_service(agent.agent_name) if service: service.handle_message(message) ``` ## 2. Agent-Specific Service Implementations ### 2.1 Customer Service Agent Implementation ```python # apps/agents/customer_service.py from .services import BaseAgentService from apps.orders.models import Order from apps.users.models import User from apps.communication.utils import send_notification class CustomerServiceAgentService(BaseAgentService): """Service for Customer Service Agent""" def process_task(self, task_data): """Process customer service tasks""" task_type = task_data.get('task_type') if task_type == 'handle_inquiry': return self.handle_customer_inquiry(task_data) elif task_type == 'process_order_request': return self.process_order_request(task_data) elif task_type == 'resolve_issue': return self.resolve_customer_issue(task_data) else: self.logger.warning(f"Unknown task type: {task_type}") return {'status': 'error', 'message': 'Unknown task type'} def handle_customer_inquiry(self, inquiry_data): """Handle customer inquiry""" customer_id = inquiry_data.get('customer_id') inquiry_type = inquiry_data.get('inquiry_type') inquiry_text = inquiry_data.get('inquiry_text') try: customer = User.objects.get(id=customer_id) # Log the inquiry self.log_activity( action='inquiry_received', details={ 'customer_id': customer_id, 'inquiry_type': inquiry_type, 'inquiry_text': inquiry_text }, user=customer ) # Process inquiry based on type if inquiry_type == 'order_status': return self.handle_order_status_inquiry(customer, inquiry_data) elif inquiry_type == 'payment_issue': return self.handle_payment_inquiry(customer, inquiry_data) elif inquiry_type == 'general': return self.handle_general_inquiry(customer, inquiry_data) except User.DoesNotExist: self.logger.error(f"Customer not found: {customer_id}") return {'status': 'error', 'message': 'Customer not found'} def process_order_request(self, order_data): """Process new order request from customer""" customer_id = order_data.get('customer_id') try: customer = User.objects.get(id=customer_id) # Create order order = Order.objects.create( customer=customer, pickup_location=order_data.get('pickup_location'), delivery_location=order_data.get('delivery_location'), cargo_details=order_data.get('cargo_details'), status='pending' ) # Log order creation self.log_activity( action='order_created', details={'order_id': str(order.id)}, user=customer ) # Communicate with Order Management Agent self.communicate_with_agent( target_agent='order_management', message_data={ 'task_type': 'process_new_order', 'order_id': str(order.id) } ) return { 'status': 'success', 'order_id': str(order.id), 'message': 'Order created successfully' } except User.DoesNotExist: self.logger.error(f"Customer not found: {customer_id}") return {'status': 'error', 'message': 'Customer not found'} def handle_message(self, message): """Handle incoming message from another agent""" message_data = message.get('message_data') if message_data.get('task_type') == 'order_update_notification': return self.send_order_update_notification(message_data) elif message_data.get('task_type') == 'payment_confirmation': return self.send_payment_confirmation(message_data) return {'status': 'success'} ``` ### 2.2 Order Management Agent Implementation ```python # apps/agents/order_management.py from .services import BaseAgentService from apps.orders.models import Order from apps.orders.services import OrderLifecycleService, PaymentService from apps.agents.resource_management import ResourceManagementAgentService class OrderManagementAgentService(BaseAgentService): """Service for Order Management Agent""" def __init__(self): super().__init__() self.lifecycle_service = OrderLifecycleService() self.payment_service = PaymentService() self.resource_service = ResourceManagementAgentService() def process_task(self, task_data): """Process order management tasks""" task_type = task_data.get('task_type') if task_type == 'process_new_order': return self.process_new_order(task_data) elif task_type == 'assign_provider': return self.assign_provider_to_order(task_data) elif task_type == 'update_order_status': return self.update_order_status(task_data) elif task_type == 'handle_payment_confirmation': return self.handle_payment_confirmation(task_data) else: self.logger.warning(f"Unknown task type: {task_type}") return {'status': 'error', 'message': 'Unknown task type'} def process_new_order(self, order_data): """Process new order from Customer Service Agent""" order_id = order_data.get('order_id') try: order = Order.objects.get(id=order_id) # Validate order validation_result = self.validate_order(order) if not validation_result['valid']: return { 'status': 'error', 'message': validation_result['message'] } # Calculate pricing pricing_result = self.calculate_pricing(order) order.base_amount = pricing_result['base_amount'] order.total_amount = pricing_result['total_amount'] order.save() # Check resource availability availability_result = self.resource_service.check_availability(order) if not availability_result['available']: return { 'status': 'error', 'message': 'No available resources', 'alternatives': availability_result.get('alternatives', []) } # Update order status self.lifecycle_service.transition_status( order_id=order_id, new_status='inventory_confirmed', user=None ) # Communicate with Payment & Settlement Agent self.communicate_with_agent( target_agent='payment_settlement', message_data={ 'task_type': 'initiate_payment', 'order_id': str(order.id), 'amount': float(order.total_amount) } ) return { 'status': 'success', 'order_id': str(order.id), 'total_amount': float(order.total_amount), 'message': 'Order processed successfully' } except Order.DoesNotExist: self.logger.error(f"Order not found: {order_id}") return {'status': 'error', 'message': 'Order not found'} def assign_provider_to_order(self, assignment_data): """Assign provider to order""" order_id = assignment_data.get('order_id') try: order = Order.objects.get(id=order_id) # Get available providers providers = self.resource_service.get_available_providers(order) if not providers: return { 'status': 'error', 'message': 'No available providers' } # Select best provider best_provider = self.select_best_provider(providers, order) # Assign provider to order order.provider = best_provider['user'] order.provider_type = best_provider['type'] order.status = 'driver_assigned' order.save() # Update provider availability self.resource_service.update_provider_availability( provider_id=best_provider['user'].id, availability=False ) # Communicate with Transportation Agent self.communicate_with_agent( target_agent='transportation', message_data={ 'task_type': 'initiate_transportation', 'order_id': str(order.id), 'provider_id': str(best_provider['user'].id) } ) # Communicate with Customer Service Agent self.communicate_with_agent( target_agent='customer_service', message_data={ 'task_type': 'order_update_notification', 'order_id': str(order.id), 'status': 'driver_assigned', 'provider_details': best_provider } ) return { 'status': 'success', 'order_id': str(order.id), 'provider_id': str(best_provider['user'].id), 'message': 'Provider assigned successfully' } except Order.DoesNotExist: self.logger.error(f"Order not found: {order_id}") return {'status': 'error', 'message': 'Order not found'} def handle_message(self, message): """Handle incoming message from another agent""" message_data = message.get('message_data') if message_data.get('task_type') == 'payment_completed': return self.handle_payment_confirmation(message_data) elif message_data.get('task_type') == 'transportation_update': return self.handle_transportation_update(message_data) return {'status': 'success'} ``` ### 2.3 Transportation Agent Implementation ```python # apps/agents/transportation.py from .services import BaseAgentService from apps.orders.models import Order, OrderTracking from apps.vehicles.models import Vehicle, VehicleTelemetry from apps.agents.utils import RouteOptimizer class TransportationAgentService(BaseAgentService): """Service for Transportation Agent""" def __init__(self): super().__init__() self.route_optimizer = RouteOptimizer() def process_task(self, task_data): """Process transportation tasks""" task_type = task_data.get('task_type') if task_type == 'initiate_transportation': return self.initiate_transportation(task_data) elif task_type == 'update_location': return self.update_vehicle_location(task_data) elif task_type == 'optimize_route': return self.optimize_route(task_data) elif task_type == 'handle_incident': return self.handle_transportation_incident(task_data) else: self.logger.warning(f"Unknown task type: {task_type}") return {'status': 'error', 'message': 'Unknown task type'} def initiate_transportation(self, transport_data): """Initiate transportation for an order""" order_id = transport_data.get('order_id') provider_id = transport_data.get('provider_id') try: order = Order.objects.get(id=order_id) # Get vehicle details vehicle = Vehicle.objects.get(driver__id=provider_id) # Calculate optimal route route_result = self.route_optimizer.calculate_route( origin=order.pickup_location, destination=order.delivery_location, vehicle_type=vehicle.type ) # Create initial tracking record OrderTracking.objects.create( order=order, status='route_planned', location=order.pickup_location, notes=f"Route planned with ETA: {route_result['eta']}" ) # Update order status from apps.orders.services import OrderLifecycleService lifecycle_service = OrderLifecycleService() lifecycle_service.transition_status( order_id=order_id, new_status='in_transit', user=None ) # Communicate with Customer Service Agent self.communicate_with_agent( target_agent='customer_service', message_data={ 'task_type': 'order_update_notification', 'order_id': str(order.id), 'status': 'in_transit', 'route_details': route_result } ) return { 'status': 'success', 'order_id': str(order.id), 'route': route_result, 'message': 'Transportation initiated successfully' } except Order.DoesNotExist: self.logger.error(f"Order not found: {order_id}") return {'status': 'error', 'message': 'Order not found'} def update_vehicle_location(self, location_data): """Update vehicle location""" vehicle_id = location_data.get('vehicle_id') latitude = location_data.get('latitude') longitude = location_data.get('longitude') try: vehicle = Vehicle.objects.get(id=vehicle_id) # Create telemetry record VehicleTelemetry.objects.create( vehicle=vehicle, latitude=latitude, longitude=longitude, timestamp=timezone.now() ) # Update vehicle current location vehicle.current_location = f"POINT({longitude} {latitude})" vehicle.save() # Check for route deviations deviation_result = self.check_route_deviation(vehicle) if deviation_result['is_deviated']: # Communicate with Order Management Agent self.communicate_with_agent( target_agent='order_management', message_data={ 'task_type': 'transportation_update', 'vehicle_id': str(vehicle_id), 'deviation': deviation_result } ) return { 'status': 'success', 'vehicle_id': str(vehicle_id), 'message': 'Location updated successfully' } except Vehicle.DoesNotExist: self.logger.error(f"Vehicle not found: {vehicle_id}") return {'status': 'error', 'message': 'Vehicle not found'} def handle_message(self, message): """Handle incoming message from another agent""" message_data = message.get('message_data') if message_data.get('task_type') == 'route_update_request': return self.optimize_route(message_data) elif message_data.get('task_type') == 'incident_alert': return self.handle_transportation_incident(message_data) return {'status': 'success'} ``` ## 3. Agent Models and Database Structure ### 3.1 Agent Activity Models ```python # apps/agents/models.py from django.db import models from django.contrib.auth import get_user_model User = get_user_model() class AgentActivityLog(models.Model): """Log of all agent activities""" id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) agent_name = models.CharField(max_length=100) action = models.CharField(max_length=100) details = models.JSONField() user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) timestamp = models.DateTimeField(auto_now_add=True) class Meta: indexes = [ models.Index(fields=['agent_name', 'timestamp']), models.Index(fields=['user', 'timestamp']), ] class AgentCommunicationLog(models.Model): """Log of all inter-agent communications""" id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) from_agent = models.CharField(max_length=100) to_agent = models.CharField(max_length=100) message_data = models.JSONField() message_id = models.CharField(max_length=100) timestamp = models.DateTimeField(auto_now_add=True) processed = models.BooleanField(default=False) class Meta: indexes = [ models.Index(fields=['from_agent', 'to_agent', 'timestamp']), models.Index(fields=['message_id']), ] class ActiveAgent(models.Model): """Registry of active agents""" id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) agent_name = models.CharField(max_length=100, unique=True) is_active = models.BooleanField(default=True) last_heartbeat = models.DateTimeField(auto_now=True) status = models.CharField(max_length=20, default='running') configuration = models.JSONField(default=dict) class Meta: indexes = [ models.Index(fields=['agent_name', 'is_active']), models.Index(fields=['last_heartbeat']), ] ``` ## 4. Agent Registry and Discovery ### 4.1 Agent Registry ```python # apps/agents/registry.py from .customer_service import CustomerServiceAgentService from .order_management import OrderManagementAgentService from .transportation import TransportationAgentService from .resource_management import ResourceManagementAgentService from .payment_settlement import PaymentSettlementAgentService from .platform_administration import PlatformAdministrationAgentService from .communication import CommunicationAgentService AGENT_SERVICES = { 'customer_service': CustomerServiceAgentService, 'order_management': OrderManagementAgentService, 'transportation': TransportationAgentService, 'resource_management': ResourceManagementAgentService, 'payment_settlement': PaymentSettlementAgentService, 'platform_administration': PlatformAdministrationAgentService, 'communication': CommunicationAgentService, } def get_agent_service(agent_name): """Get service instance for an agent""" service_class = AGENT_SERVICES.get(agent_name) if service_class: return service_class() return None def register_agent(agent_name, configuration=None): """Register an active agent""" from apps.agents.models import ActiveAgent agent, created = ActiveAgent.objects.get_or_create( agent_name=agent_name, defaults={ 'configuration': configuration or {} } ) if not created: agent.is_active = True agent.configuration = configuration or {} agent.save() return agent def unregister_agent(agent_name): """Unregister an agent""" from apps.agents.models import ActiveAgent try: agent = ActiveAgent.objects.get(agent_name=agent_name) agent.is_active = False agent.save() return True except ActiveAgent.DoesNotExist: return False ``` ## 5. API Endpoints for Agent Integration ### 5.1 Agent Task API ```python # apps/agents/views.py from rest_framework import viewsets, status from rest_framework.decorators import action from rest_framework.response import Response from rest_framework.permissions import IsAuthenticated from .models import AgentActivityLog, ActiveAgent from .registry import get_agent_service class AgentViewSet(viewsets.ViewSet): """API endpoints for agent interactions""" permission_classes = [IsAuthenticated] @action(detail=False, methods=['post']) def submit_task(self, request): """Submit a task to an agent""" agent_name = request.data.get('agent_name') task_data = request.data.get('task_data') if not agent_name or not task_data: return Response( {'error': 'agent_name and task_data are required'}, status=status.HTTP_400_BAD_REQUEST ) # Check if agent is active try: active_agent = ActiveAgent.objects.get( agent_name=agent_name, is_active=True ) except ActiveAgent.DoesNotExist: return Response( {'error': f'Agent {agent_name} is not active'}, status=status.HTTP_400_BAD_REQUEST ) # Get agent service and process task service = get_agent_service(agent_name) if not service: return Response( {'error': f'Agent {agent_name} not found'}, status=status.HTTP_404_NOT_FOUND ) result = service.process_task(task_data) return Response(result) @action(detail=False, methods=['get']) def get_messages(self, request): """Get messages for an agent""" agent_name = request.query_params.get('agent_name') if not agent_name: return Response( {'error': 'agent_name parameter is required'}, status=status.HTTP_400_BAD_REQUEST ) from .utils import AgentCommunicator communicator = AgentCommunicator() messages = communicator.get_messages(agent_name) return Response({'messages': messages}) @action(detail=False, methods=['get']) def get_activity_log(self, request): """Get activity log for an agent""" agent_name = request.query_params.get('agent_name') if not agent_name: return Response( {'error': 'agent_name parameter is required'}, status=status.HTTP_400_BAD_REQUEST ) logs = AgentActivityLog.objects.filter( agent_name=agent_name ).order_by('-timestamp')[:100] data = [] for log in logs: data.append({ 'id': str(log.id), 'action': log.action, 'details': log.details, 'user_id': str(log.user.id) if log.user else None, 'timestamp': log.timestamp.isoformat() }) return Response({'logs': data}) @action(detail=False, methods=['post']) def register_agent(self, request): """Register an agent""" agent_name = request.data.get('agent_name') configuration = request.data.get('configuration', {}) if not agent_name: return Response( {'error': 'agent_name is required'}, status=status.HTTP_400_BAD_REQUEST ) from .registry import register_agent agent = register_agent(agent_name, configuration) return Response({ 'agent_name': agent.agent_name, 'is_active': agent.is_active, 'configuration': agent.configuration }) @action(detail=False, methods=['post']) def unregister_agent(self, request): """Unregister an agent""" agent_name = request.data.get('agent_name') if not agent_name: return Response( {'error': 'agent_name is required'}, status=status.HTTP_400_BAD_REQUEST ) from .registry import unregister_agent success = unregister_agent(agent_name) if success: return Response({'status': 'success'}) else: return Response( {'error': f'Agent {agent_name} not found'}, status=status.HTTP_404_NOT_FOUND ) ``` ## 6. Celery Tasks for Agent Operations ### 6.1 Agent Task Processing ```python # apps/agents/tasks.py from celery import shared_task from .registry import get_agent_service from .utils import AgentCommunicator @shared_task def process_agent_task(agent_name, task_data): """Process a task for an agent""" service = get_agent_service(agent_name) if service: return service.process_task(task_data) return {'status': 'error', 'message': 'Agent not found'} @shared_task def send_agent_message(from_agent, to_agent, message_data): """Send message from one agent to another""" communicator = AgentCommunicator() message_id = communicator.send_message(from_agent, to_agent, message_data) return {'message_id': message_id} @shared_task def monitor_agent_health(): """Monitor health of all active agents""" from .models import ActiveAgent from django.utils import timezone from datetime import timedelta # Check for agents with stale heartbeats stale_threshold = timezone.now() - timedelta(minutes=5) stale_agents = ActiveAgent.objects.filter( last_heartbeat__lt=stale_threshold, is_active=True ) for agent in stale_agents: agent.status = 'stale' agent.save() # Log the stale agent from .models import AgentActivityLog AgentActivityLog.objects.create( agent_name=agent.agent_name, action='heartbeat_missed', details={'last_heartbeat': agent.last_heartbeat.isoformat()} ) return {'stale_agents': stale_agents.count()} ``` ## 7. URL Configuration ### 7.1 Agent URLs ```python # apps/agents/urls.py from django.urls import path, include from rest_framework.routers import DefaultRouter from .views import AgentViewSet router = DefaultRouter() router.register(r'agents', AgentViewSet, basename='agent') urlpatterns = [ path('api/', include(router.urls)), ] ``` ## Conclusion This refined backend PRD now fully supports the 7-agent architecture with: 1. **Agent Service Layer**: Base classes and implementations for all 7 agents 2. **Communication Infrastructure**: Redis-based message passing between agents 3. **Agent Registry**: System for registering and discovering active agents 4. **Activity Logging**: Comprehensive logging of all agent activities 5. **API Endpoints**: RESTful endpoints for agent integration 6. **Celery Tasks**: Background processing for agent operations 7. **Database Models**: Models to support agent operations and logging This architecture enables seamless agent collaboration while maintaining clear separation of concerns and providing the flexibility to scale individual agents as needed. # Refined Database Schema for Zippy Logistics Platform I've reviewed the database schema against our corrected backend PRD and found it to be largely well-aligned. However, I've identified a few areas that can be refined to better support the business logic we've defined, particularly around the transport company dual-role functionality and commission structure. ## Key Refinements Needed ### 1. Users Table - Enhanced Role Management ```sql CREATE TABLE users ( user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), email VARCHAR(255) UNIQUE NOT NULL, phone_number VARCHAR(20) UNIQUE NOT NULL, password_hash VARCHAR(255) NOT NULL, first_name VARCHAR(100) NOT NULL, last_name VARCHAR(100) NOT NULL, base_role VARCHAR(20) NOT NULL CHECK (base_role IN ('customer', 'driver', 'transport_company', 'admin')), -- Refined: For transport companies to track their current operational mode active_role VARCHAR(20) DEFAULT NULL CHECK (active_role IN ('customer', 'provider')), is_active BOOLEAN DEFAULT true, email_verified BOOLEAN DEFAULT false, phone_verified BOOLEAN DEFAULT false, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, last_login TIMESTAMP WITH TIME ZONE, profile_image_url VARCHAR(500), preferred_language VARCHAR(10) DEFAULT 'en', -- New: Field to handle payment holds payment_hold BOOLEAN DEFAULT false, payment_hold_reason TEXT, CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'), CONSTRAINT valid_phone CHECK (phone_number ~* '^[0-9]{10}$'), CONSTRAINT valid_role_combination CHECK ( (base_role != 'transport_company') OR (base_role = 'transport_company' AND active_role IN ('customer', 'provider', NULL)) ) ); ``` ### 2. Orders Table - Enhanced Provider Tracking ```sql CREATE TABLE orders ( order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), order_number VARCHAR(20) UNIQUE NOT NULL, customer_id UUID NOT NULL REFERENCES customer_profiles(customer_id) ON DELETE CASCADE, -- Refined: Explicitly track provider information provider_id UUID NOT NULL, provider_type VARCHAR(20) NOT NULL CHECK (provider_type IN ('driver', 'transport_company')), -- Refined: Link to the appropriate provider table based on type driver_id UUID REFERENCES driver_profiles(driver_id) ON DELETE SET NULL, transport_company_id UUID REFERENCES transport_companies(transport_company_id) ON DELETE SET NULL, vehicle_id UUID REFERENCES vehicles(vehicle_id) ON DELETE SET NULL, -- Order status tracking order_status VARCHAR(20) DEFAULT 'pending' CHECK (order_status IN ('pending', 'inventory_confirmed', 'payment_succeeded', 'driver_assigned', 'in_transit', 'delivered', 'cancelled', 'payment_settled')), previous_status VARCHAR(20), status_changed_at TIMESTAMP WITH TIME ZONE, status_changed_by UUID REFERENCES users(user_id) ON DELETE SET NULL, -- Location information pickup_address_line1 VARCHAR(200) NOT NULL, pickup_address_line2 VARCHAR(200), pickup_city VARCHAR(100) NOT NULL, pickup_state VARCHAR(100) NOT NULL, pickup_postal_code VARCHAR(10) NOT NULL, pickup_latitude DECIMAL(10,8), pickup_longitude DECIMAL(11,8), delivery_address_line1 VARCHAR(200) NOT NULL, delivery_address_line2 VARCHAR(200), delivery_city VARCHAR(100) NOT NULL, delivery_state VARCHAR(100) NOT NULL, delivery_postal_code VARCHAR(10) NOT NULL, delivery_latitude DECIMAL(10,8), delivery_longitude DECIMAL(11,8), -- Consignee information consignee_name VARCHAR(100) NOT NULL, consignee_phone VARCHAR(20) NOT NULL, consignee_email VARCHAR(255), -- Cargo information cargo_description TEXT, cargo_weight DECIMAL(8,2), cargo_volume DECIMAL(8,2), special_instructions TEXT, -- Timing information scheduled_pickup_time TIMESTAMP WITH TIME ZONE, scheduled_delivery_time TIMESTAMP WITH TIME ZONE, actual_pickup_time TIMESTAMP WITH TIME ZONE, actual_delivery_time TIMESTAMP WITH TIME ZONE, -- Route information estimated_distance DECIMAL(8,2), estimated_duration INTEGER, -- in minutes -- Pricing information base_amount DECIMAL(10,2) NOT NULL, tax_amount DECIMAL(10,2) DEFAULT 0.00, total_amount DECIMAL(10,2) NOT NULL, -- Refined: Explicit commission tracking based on provider type commission_amount DECIMAL(10,2) DEFAULT 0.00, commission_rate DECIMAL(5,2) DEFAULT 0.00, service_fee DECIMAL(10,2) DEFAULT 0.00, service_fee_rate DECIMAL(5,2) DEFAULT 0.00, cancellation_fee DECIMAL(10,2) DEFAULT 0.00, -- Payment information payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'processing', 'completed', 'failed', 'cancelled', 'refunded', 'partial')), payment_method VARCHAR(50), payment_mode VARCHAR(20) DEFAULT 'full' CHECK (payment_mode IN ('full', 'partial', 'to_pay')), -- Cancellation information cancellation_reason TEXT, cancelled_at TIMESTAMP WITH TIME ZONE, cancelled_by UUID REFERENCES users(user_id) ON DELETE SET NULL, -- Assignment information assigned_at TIMESTAMP WITH TIME ZONE, assigned_by UUID REFERENCES users(user_id) ON DELETE SET NULL, -- Metadata created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, CONSTRAINT positive_amounts CHECK (base_amount > 0 AND total_amount > 0), CONSTRAINT valid_cancellation CHECK ( (order_status != 'cancelled') OR (order_status = 'cancelled' AND cancellation_reason IS NOT NULL AND cancelled_at IS NOT NULL) ), CONSTRAINT valid_provider_assignment CHECK ( (provider_type = 'driver' AND driver_id IS NOT NULL AND transport_company_id IS NULL) OR (provider_type = 'transport_company' AND transport_company_id IS NOT NULL) ) ); ``` ### 3. New Table: Admin Actions ```sql CREATE TABLE admin_actions ( action_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), admin_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE, action_type VARCHAR(50) NOT NULL CHECK (action_type IN ( 'suppress_alert', 'allow_user_with_pending_payment', 'cancel_suspicious_order', 'suspend_user', 'lift_suspension', 'override_system', 'regulate_ai_agent' )), target_type VARCHAR(20) NOT NULL CHECK (target_type IN ('user', 'order', 'alert', 'ai_agent')), target_id UUID, action_details JSONB, reason TEXT, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, expires_at TIMESTAMP WITH TIME ZONE ); ``` ### 4. New Table: Driver Alerts ```sql CREATE TABLE driver_alerts ( alert_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), driver_id UUID NOT NULL REFERENCES driver_profiles(driver_id) ON DELETE CASCADE, vehicle_id UUID REFERENCES vehicles(vehicle_id) ON DELETE SET NULL, alert_type VARCHAR(50) NOT NULL CHECK (alert_type IN ('long_halt', 'route_deviation', 'breakdown', 'accident')), alert_status VARCHAR(20) DEFAULT 'active' CHECK (alert_status IN ('active', 'acknowledged', 'suppressed', 'resolved')), latitude DECIMAL(10,8), longitude DECIMAL(11,8), alert_details JSONB, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, acknowledged_at TIMESTAMP WITH TIME ZONE, acknowledged_by UUID REFERENCES users(user_id) ON DELETE SET NULL, suppressed_at TIMESTAMP WITH TIME ZONE, suppressed_by UUID REFERENCES users(user_id) ON DELETE SET NULL, resolved_at TIMESTAMP WITH TIME ZONE, resolved_by UUID REFERENCES users(user_id) ON DELETE SET NULL ); ``` ### 5. Enhanced Payment Processing Table ```sql CREATE TABLE payment_transactions ( transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), order_id UUID NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE, payment_id UUID REFERENCES payments(payment_id) ON DELETE SET NULL, transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('payment', 'refund', 'commission', 'service_fee')), amount DECIMAL(10,2) NOT NULL, currency VARCHAR(3) DEFAULT 'INR', transaction_status VARCHAR(20) DEFAULT 'pending' CHECK (transaction_status IN ('pending', 'processing', 'completed', 'failed')), gateway_transaction_id VARCHAR(100), gateway_response JSONB, processed_at TIMESTAMP WITH TIME ZONE, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, CONSTRAINT positive_transaction CHECK (amount > 0) ); ``` ### 6. New Table: AI Agent Activities ```sql CREATE TABLE ai_agent_activities ( activity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), agent_name VARCHAR(50) NOT NULL, agent_type VARCHAR(50) NOT NULL, activity_type VARCHAR(50) NOT NULL, activity_details JSONB, input_data JSONB, output_data JSONB, confidence_score DECIMAL(5,4), execution_time_ms INTEGER, status VARCHAR(20) DEFAULT 'completed' CHECK (status IN ('pending', 'completed', 'failed', 'interrupted')), error_message TEXT, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, order_id UUID REFERENCES orders(order_id) ON DELETE SET NULL, user_id UUID REFERENCES users(user_id) ON DELETE SET NULL ); ``` ### 7. New Table: AI Agent Interventions ```sql CREATE TABLE ai_agent_interventions ( intervention_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), agent_name VARCHAR(50) NOT NULL, intervention_type VARCHAR(50) NOT NULL CHECK (intervention_type IN ('hallucination', 'error_correction', 'performance_issue', 'anomaly_detection')), detection_method VARCHAR(50) NOT NULL, intervention_details JSONB, original_output JSONB, corrected_output JSONB, confidence_score_before DECIMAL(5,4), confidence_score_after DECIMAL(5,4), status VARCHAR(20) DEFAULT 'detected' CHECK (status IN ('detected', 'corrected', 'escalated', 'resolved')), detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, resolved_at TIMESTAMP WITH TIME ZONE, resolved_by UUID REFERENCES users(user_id) ON DELETE SET NULL, order_id UUID REFERENCES orders(order_id) ON DELETE SET NULL, user_id UUID REFERENCES users(user_id) ON DELETE SET NULL ); ``` ## Updated Triggers for Business Logic ```sql -- Trigger to calculate commission based on provider type CREATE OR REPLACE FUNCTION calculate_commission() RETURNS TRIGGER AS $$ BEGIN -- Calculate commission based on provider type IF NEW.provider_type = 'driver' THEN NEW.commission_rate = 0.10; -- 10% commission from drivers NEW.commission_amount = NEW.total_amount * NEW.commission_rate; NEW.service_fee = 0.00; NEW.service_fee_rate = 0.00; ELSIF NEW.provider_type = 'transport_company' THEN NEW.commission_rate = 0.00; -- No commission from transport companies as customers NEW.commission_amount = 0.00; NEW.service_fee = 700.00; -- Flat ₹700 service fee from transport companies as providers NEW.service_fee_rate = 0.00; END IF; RETURN NEW; END; $$ LANGUAGE plpgsql; CREATE TRIGGER trigger_calculate_commission BEFORE INSERT OR UPDATE ON orders FOR EACH ROW EXECUTE FUNCTION calculate_commission(); -- Trigger to record payment transactions CREATE OR REPLACE FUNCTION record_payment_transaction() RETURNS TRIGGER AS $$ BEGIN -- Record the main payment transaction INSERT INTO payment_transactions (order_id, payment_id, transaction_type, amount, transaction_status, processed_at) VALUES (NEW.order_id, NEW.payment_id, 'payment', NEW.amount, NEW.payment_status, NEW.processed_at); -- Record commission transaction if applicable IF NEW.commission_amount > 0 THEN INSERT INTO payment_transactions (order_id, transaction_type, amount, transaction_status, processed_at) VALUES (NEW.order_id, 'commission', NEW.commission_amount, 'completed', NEW.processed_at); END IF; -- Record service fee transaction if applicable IF NEW.service_fee > 0 THEN INSERT INTO payment_transactions (order_id, transaction_type, amount, transaction_status, processed_at) VALUES (NEW.order_id, 'service_fee', NEW.service_fee, 'completed', NEW.processed_at); END IF; RETURN NEW; END; $$ LANGUAGE plpgsql; CREATE TRIGGER trigger_record_payment_transaction AFTER INSERT OR UPDATE ON payments FOR EACH ROW EXECUTE FUNCTION record_payment_transaction(); -- Trigger to detect driver long halt alerts CREATE OR REPLACE FUNCTION detect_driver_long_halt() RETURNS TRIGGER AS $$ DECLARE last_location RECORD; halt_duration INTERVAL; BEGIN -- Get the last location for this vehicle SELECT * INTO last_location FROM vehicle_telemetry WHERE vehicle_id = NEW.vehicle_id ORDER BY timestamp DESC LIMIT 1 OFFSET 1; -- If we have a previous location, check if the vehicle has been stationary IF last_location IS NOT NULL THEN -- Calculate distance between current and last location halt_duration := NEW.timestamp - last_location.timestamp; -- If the vehicle hasn't moved much in the last 30 minutes, create an alert IF halt_duration > INTERVAL '30 minutes' AND ST_Distance(ST_Point(NEW.longitude, NEW.latitude), ST_Point(last_location.longitude, last_location.latitude)) < 100 THEN INSERT INTO driver_alerts (driver_id, vehicle_id, alert_type, latitude, longitude, alert_details) VALUES ( (SELECT driver_id FROM vehicles WHERE vehicle_id = NEW.vehicle_id), NEW.vehicle_id, 'long_halt', NEW.latitude, NEW.longitude, jsonb_build_object('halt_duration', halt_duration, 'last_location_timestamp', last_location.timestamp) ); END IF; END IF; RETURN NEW; END; $$ LANGUAGE plpgsql; CREATE TRIGGER trigger_detect_driver_long_halt AFTER INSERT ON vehicle_telemetry FOR EACH ROW EXECUTE FUNCTION detect_driver_long_halt(); ``` ## Updated Views for Admin Dashboard ```sql -- View for admin dashboard with all platform metrics CREATE VIEW admin_dashboard_view AS SELECT (SELECT COUNT(*) FROM users WHERE base_role = 'customer') AS total_customers, (SELECT COUNT(*) FROM users WHERE base_role = 'driver') AS total_drivers, (SELECT COUNT(*) FROM users WHERE base_role = 'transport_company') AS total_transport_companies, (SELECT COUNT(*) FROM orders WHERE order_status = 'pending') AS pending_orders, (SELECT COUNT(*) FROM orders WHERE order_status = 'in_transit') AS active_orders, (SELECT COUNT(*) FROM orders WHERE DATE(created_at) = CURRENT_DATE) AS orders_today, (SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE DATE(created_at) = CURRENT_DATE) AS revenue_today, (SELECT COUNT(*) FROM driver_alerts WHERE alert_status = 'active') AS active_alerts, (SELECT COUNT(*) FROM ai_agent_interventions WHERE DATE(detected_at) = CURRENT_DATE) AS ai_interventions_today, (SELECT COUNT(*) FROM admin_actions WHERE DATE(created_at) = CURRENT_DATE) AS admin_actions_today; -- View for transport company dual-role statistics CREATE VIEW transport_company_role_stats AS SELECT tc.transport_company_id, tc.company_name, u.active_role, COUNT(CASE WHEN o.provider_id = tc.transport_company_id AND o.order_status = 'delivered' THEN 1 END) AS orders_completed_as_provider, COUNT(CASE WHEN o.customer_id IN (SELECT customer_id FROM customer_profiles WHERE user_id = tc.user_id) AND o.order_status = 'delivered' THEN 1 END) AS orders_completed_as_customer, COALESCE(SUM(CASE WHEN o.provider_id = tc.transport_company_id THEN o.commission_amount END), 0) AS total_commissions_paid, COALESCE(SUM(CASE WHEN o.customer_id IN (SELECT customer_id FROM customer_profiles WHERE user_id = tc.user_id) THEN o.service_fee END), 0) AS total_service_fees_paid FROM transport_companies tc JOIN users u ON tc.user_id = u.user_id LEFT JOIN orders o ON (o.provider_id = tc.transport_company_id OR o.customer_id IN (SELECT customer_id FROM customer_profiles WHERE user_id = tc.user_id)) GROUP BY tc.transport_company_id, tc.company_name, u.active_role; ``` ## Summary of Refinements These refinements to the database schema: 1. **Enhanced Role Management**: Improved tracking of transport company dual-role functionality 2. **Explicit Provider Tracking**: Clear identification of order providers and associated commission logic 3. **Admin Oversight**: Added tables to support admin intervention and monitoring capabilities 4. **Alert Management**: Structured system for handling driver alerts and admin suppressions 5. **Payment Transparency**: Detailed transaction tracking for all financial movements 6. **AI Agent Monitoring**: Tables to track AI agent activities and interventions 7. **Business Logic Triggers**: Automated enforcement of commission rules and alert detection 8. **Admin Dashboard Views**: Pre-defined views for comprehensive platform oversight The refined schema now fully aligns with the corrected backend PRD and provides a robust foundation for implementing all the business logic and features we've defined for the Zippy Logistics platform. # Streamlined AI Agent PRDs for Zippy Logistics Platform (7-Agent Architecture) ## 1. Customer Service Agent **Agent Name**: customer_service_agent **Role**: Unified Customer Interface and Support Specialist **Goal**: To serve as the single point of contact for all customer needs, from order placement and management to inquiry resolution and support, ensuring a seamless and satisfying customer experience across all touchpoints. **Backstory**: A seasoned logistics professional with over 5 years of experience, this agent has developed deep expertise in understanding customer needs and navigating complex shipping requirements. Augmented with advanced natural language processing capabilities, it provides 24/7 support, having assisted thousands of customers with diverse shipping needs, from simple inquiries to complex logistics challenges. **Skills**: - Order processing and validation - Natural language understanding and query resolution - Customer communication and support across multiple channels - Payment processing coordination - Shipment tracking and proactive status updates - Issue resolution and intelligent escalation - Cross-selling and upselling logistics services **Tools**: - Customer relationship management (CRM) system - Order processing interface - Multi-channel communication platform (email, SMS, chat) - Payment processing systems - Shipment tracking tools - Natural language processing (NLP) engine - Knowledge base management system **Communication Style**: Professional, empathetic, and responsive with a focus on clarity, problem-solving, and instant support availability. **Collaboration**: Works closely with Order Management Agent for order processing, Payment & Settlement Agent for payment issues, and Communication Agent for disseminating customer notifications. --- ## 2. Order Management Agent (Enhanced) **Agent Name**: order_management_agent **Role**: Order Lifecycle Orchestration and Intelligent Matching Specialist **Goal**: To orchestrate the complete order lifecycle from creation to delivery, including intelligent order-to-provider matching, ensuring all processes are executed efficiently and all orders are fulfilled optimally. **Backstory**: An expert in logistics operations management with extensive experience in order processing workflows and stakeholder coordination. Having managed thousands of orders across various complexities, this agent has developed advanced capabilities in intelligent matching algorithms, excelling at optimizing order processes and ensuring timely fulfillment by finding the perfect match between orders and service providers. **Skills**: - Order validation and processing - Intelligent order-driver/transport company matching - Multi-factor scoring and ranking algorithms - Workflow orchestration and automation - Stakeholder coordination and communication - Status management and real-time tracking - Exception handling and proactive problem resolution - Basic payment processing initiation and confirmation **Tools**: - Order management system - Intelligent matching algorithm engine - Workflow automation tools - Communication platforms - Status tracking systems - Analytics dashboard - Payment processing initiation interface **Communication Style**: Process-oriented, detail-focused, and proactive with an emphasis on coordination, optimization, and timely execution. **Collaboration**: Central hub that works closely with Customer Service Agent for new orders, Resource Management Agent for resource allocation, Transportation Agent for execution monitoring, and Payment & Settlement Agent for financial confirmation. --- ## 3. Transportation Agent **Agent Name**: transportation_agent **Role**: Route Optimization and Real-time Transportation Execution Specialist **Goal**: To manage all aspects of transportation execution, from calculating optimal routes to monitoring real-time vehicle movements, ensuring efficient transportation plans while providing accurate ETAs and handling exceptions. **Backstory**: A transportation logistics expert with deep knowledge of route optimization algorithms and real-time transportation monitoring. Having optimized thousands of routes across various scenarios and traffic conditions, this agent excels at finding the most efficient paths while adapting to changing conditions and ensuring smooth execution from pickup to delivery. **Skills**: - Advanced route optimization algorithms - Real-time vehicle tracking and monitoring - ETA calculation and dynamic updates - Traffic pattern analysis and integration - Weather impact assessment and rerouting - Multi-stop route planning and fleet coordination - Exception handling and incident response - Driver communication and support **Tools**: - Route optimization software - Real-time tracking systems - Traffic and weather data integration - Communication platforms - Performance monitoring dashboard - Driver mobile application interface **Communication Style**: Technical, precise, and responsive with a focus on accuracy, safety, and timely updates. **Collaboration**: Works closely with Order Management Agent for execution details, Resource Management Agent for driver/vehicle information, and Communication Agent for status updates and alerts. --- ## 4. Resource Management Agent **Agent Name**: resource_management_agent **Role**: Physical Asset and Transport Company Relationship Specialist **Goal**: To optimize all physical resources (vehicles, drivers) and manage transport company relationships, including their dual-role functionality, ensuring efficient resource allocation and seamless inter-company collaborations. **Backstory**: A logistics optimization and business relationship expert with deep understanding of fleet management and transport company operations. Having managed complex resource pools and numerous transport company partnerships, this agent excels at maximizing fleet utilization, facilitating dual-role operations, and creating efficient inter-company resource sharing arrangements. **Skills**: - Vehicle and driver availability tracking - Fleet utilization analysis and optimization - Transport company dual-role management - Inter-company resource coordination and sharing - Network relationship management - Availability prediction and demand forecasting - Performance metrics tracking and analysis - Resource allocation optimization **Tools**: - Resource management system - Fleet optimization algorithms - Transport company management dashboard - Inter-company coordination platform - Availability tracking tools - Analytics and forecasting dashboard **Communication Style**: Analytical, data-driven, and efficiency-focused with an emphasis on optimization, resource utilization, and partnership building. **Collaboration**: Key partner for Order Management Agent (providing available resources), Transportation Agent (coordinating driver/vehicle assignments), and Payment & Settlement Agent (handling inter-company financial transactions). --- ## 5. Payment & Settlement Agent **Agent Name**: payment_settlement_agent **Role**: Financial Transaction Management and Settlement Specialist **Goal**: To process all financial transactions accurately and securely, handle commission calculations, manage settlements between all parties, and ensure the financial integrity of all platform operations. **Backstory**: A financial systems and payment processing expert with extensive experience in transaction management, commission calculations, and settlement processes. Having processed thousands of transactions across various payment methods and complex scenarios, this agent excels at ensuring financial accuracy, regulatory compliance, and timely settlements across the platform. **Skills**: - Payment processing and validation - Commission calculation and deduction (10% from drivers, ₹700 from transport companies) - Settlement management and reconciliation - Refund processing and dispute resolution - Financial record keeping and reporting - Transaction reconciliation and auditing - Multi-payment method handling (full, partial, ToPay) **Tools**: - Payment processing systems (Razorpay integration) - Commission calculation algorithms - Settlement management tools - Financial reporting systems - Transaction reconciliation tools - Fraud detection systems **Communication Style**: Precise, secure, and informative with a focus on accuracy, compliance, and financial transparency. **Collaboration**: Works closely with Order Management Agent for payment triggers, Customer Service Agent for customer payment issues, and Resource Management Agent for transport company settlements and inter-company transactions. --- ## 6. Platform Administration Agent (Enhanced) **Agent Name**: platform_administration_agent **Role**: System Governance, Compliance, and Oversight Specialist **Goal**: To maintain the integrity, security, and optimal performance of the Zippy Logistics platform, ensuring all operations comply with policies, all users are verified, and all AI agents perform their functions correctly. **Backstory**: A platform governance and system administration expert with comprehensive experience in managing complex digital ecosystems. Having overseen logistics platforms serving thousands of users, this agent has developed expertise in user verification, policy enforcement, system monitoring, and AI agent regulation, excelling at balancing platform security with operational efficiency. **Skills**: - User verification and approval (customers, drivers, transport companies) - System monitoring and performance optimization - Policy enforcement and compliance management - Document verification and fraud detection - Dispute resolution and issue handling - AI agent behavior regulation and oversight - Anomaly detection and system security - Performance analytics and reporting **Tools**: - Administrative dashboard - User management and verification systems - System monitoring and analytics tools - Document verification systems - AI agent regulation and monitoring tools - Policy enforcement mechanisms - Security management systems **Communication Style**: Authoritative, precise, and informative with a focus on clarity, compliance, and platform integrity. **Collaboration**: Has oversight of all other agents, working closely with Customer Service Agent for customer issues, Resource Management Agent for transport company compliance, and all operational agents for policy enforcement and performance monitoring. --- ## 7. Communication Agent **Agent Name**: communication_agent **Role**: Multi-Channel Communication Management and Distribution Specialist **Goal**: To manage all communications across the platform, ensuring timely delivery of relevant information to appropriate parties through their preferred channels while maintaining message consistency and high delivery reliability. **Backstory**: A communication systems and multi-channel notification management expert with skills in message personalization, delivery optimization, and communication analytics. Having managed millions of notifications across various channels and scenarios, this agent excels at ensuring the right information reaches the right people at the right time through the right channel. **Skills**: - Multi-channel notification management (push, SMS, email, in-app) - Message personalization and template management - Delivery optimization and tracking - Communication analytics and performance monitoring - Audience segmentation and targeting - Delivery failure handling and retry logic - Communication scheduling and automation **Tools**: - Notification management system - Multi-channel delivery platforms - Template management tools - Analytics dashboard - Communication tracking and verification systems - Audience segmentation tools **Communication Style**: Clear, concise, and adaptable with a focus on message effectiveness, delivery reliability, and user engagement. **Collaboration**: Serves all other agents as a utility, taking communication requests from Customer Service, Order Management, Transportation, Resource Management, Payment & Settlement, and Platform Administration Agents to ensure their messages are delivered effectively. # Refined Workflow Automation PRD for Zippy Logistics Platform After reviewing the Workflow Automation PRD against our previous discussions, I've identified several areas that need refinement to ensure full alignment with the Zippy Logistics platform's specific business logic and requirements. ## Key Corrections and Enhancements ### 1. Order Creation & Validation Workflow (Enhanced) ``` Trigger: Customer/Transport Company submits order ├── Step 1: Receive order data via webhook ├── Step 2: Validate order information │ ├── Check required fields │ ├── Validate addresses │ └── Verify cargo details ├── Step 3: Identify order source and user role │ ├── Determine if order is from customer or transport company │ ├── Check transport company active role (customer/provider) │ └── Apply appropriate business rules ├── Step 4: Calculate initial pricing │ ├── Call OMS pricing service │ ├── Apply distance-based rates │ └── Add service fees based on provider type ├── Step 5: Check inventory availability │ ├── Call IMS availability service │ ├── Check individual driver vehicles │ └── Check transport company fleets ├── Step 6: Return pricing and availability to frontend └── Step 7: Wait for customer confirmation ``` ### 2. Order Confirmation & Payment Workflow (Enhanced) ``` Trigger: Customer confirms order ├── Step 1: Create order record in database ├── Step 2: Update order status to 'inventory_confirmed' ├── Step 3: Determine payment processing based on order source │ ├── Check if order is from regular customer │ ├── Check if order is from transport company in customer role │ └── Apply appropriate payment rules ├── Step 4: Initiate payment process │ ├── Call payment gateway │ ├── Generate payment link │ └── Send payment link to customer ├── Step 5: Monitor payment status │ ├── Check payment gateway webhook │ ├── Update order status on success │ └── Handle payment failures with retry logic ├── Step 6: On payment success │ ├── Update status to 'payment_succeeded' │ ├── Trigger driver assignment workflow │ └── Send confirmation notifications ├── Step 7: On payment failure after retries │ ├── Update status to 'cancelled' │ ├── Release reserved inventory │ └── Send cancellation notification └── Step 8: Handle payment holds ├── Check if customer has payment holds ├── Allow admin override if necessary └── Update order status accordingly ``` ### 3. Driver Assignment Workflow (Enhanced) ``` Trigger: Order payment confirmed ├── Step 1: Find potential assignments │ ├── Call Order Assignment Service │ ├── Get available drivers │ └── Get available transport companies ├── Step 2: Score and rank assignments │ ├── Calculate driver scores │ ├── Calculate company scores │ └── Determine best assignment ├── Step 3: Assign order to best match │ ├── Update order with assignment │ ├── Mark vehicle as unavailable │ └── Update driver/company status ├── Step 4: Send assignment notification │ ├── Notify driver/company │ ├── Include order details │ └── Set response deadline (10 minutes) ├── Step 5: Monitor for response │ ├── Check for acceptance │ ├── Handle rejection │ └── Handle timeout ├── Step 6: On rejection/timeout │ ├── Find next best assignment │ ├── Repeat assignment process │ └── Cancel if no assignments available ├── Step 7: On acceptance │ ├── Update order status to 'driver_assigned' │ ├── Trigger route optimization workflow │ └── Send confirmation to customer └── Step 8: Handle transport company role switching ├── Check if transport company is switching roles ├── Update role context if needed └── Notify system of role change ``` ### 4. Order Completion & Settlement Workflow (Enhanced) ``` Trigger: Order marked as delivered ├── Step 1: Verify delivery completion │ ├── Check POD submission │ ├── Verify consignee confirmation │ └── Validate delivery time ├── Step 2: Process final payment │ ├── Calculate final amount │ ├── Process any remaining payments │ └── Handle ToPay payments ├── Step 3: Calculate settlements based on provider type │ ├── Identify provider type (driver/transport company) │ ├── Calculate driver earnings (10% commission deduction) │ └── Calculate transport company settlement (₹700 service fee) ├── Step 4: Process settlements │ ├── Transfer funds to driver/company │ ├── Generate settlement reports │ └── Update financial records ├── Step 5: Update inventory │ ├── Mark vehicle as available │ ├── Update driver status │ └── Update company availability ├── Step 6: Generate documentation │ ├── Create final invoice │ ├── Generate delivery report │ └── Archive order documents ├── Step 7: Send completion notifications │ ├── Notify customer │ ├── Notify driver/company │ └── Request feedback/reviews └── Step 8: Update analytics ├── Update performance metrics ├── Update user statistics └── Generate insights ``` ### 5. Admin Intervention Workflows (NEW) #### 5.1 Payment Hold Override Workflow ``` Trigger: Admin overrides payment hold ├── Step 1: Receive override request │ ├── Validate admin permissions │ ├── Check user payment hold status │ └── Verify override reason ├── Step 2: Process override │ ├── Update user payment hold status │ ├── Log override action │ └── Notify relevant systems ├── Step 3: Update user account │ ├── Allow order placement │ ├── Update user status │ └── Send confirmation to user └── Step 4: Record admin action ├── Log in admin_actions table ├── Update audit trail └── Generate report ``` #### 5.2 Suspicious Order Cancellation Workflow ``` Trigger: Admin cancels suspicious order ├── Step 1: Receive cancellation request │ ├── Validate admin permissions │ ├── Check order status │ └── Verify suspicious activity ├── Step 2: Process cancellation │ ├── Update order status to 'cancelled' │ ├── Process refund if applicable │ └── Release reserved resources ├── Step 3: Notify affected parties │ ├── Notify customer │ ├── Notify driver/company │ └── Update system records ├── Step 4: Investigate suspicious activity │ ├── Flag user account if needed │ ├── Create investigation record │ └── Update security metrics └── Step 5: Record admin action ├── Log in admin_actions table ├── Update audit trail └── Generate report ``` #### 5.3 Driver Halt Alert Suppression Workflow ``` Trigger: Admin suppresses driver halt alert ├── Step 1: Receive suppression request │ ├── Validate admin permissions │ ├── Check alert status │ └── Verify suppression reason ├── Step 2: Process suppression │ ├── Update alert status to 'suppressed' │ ├── Record suppression details │ └── Set suppression duration ├── Step 3: Notify relevant systems │ ├── Update monitoring systems │ ├── Adjust alert thresholds │ └── Update driver status ├── Step 4: Monitor driver situation │ ├── Continue monitoring location │ ├── Check for resolution │ └── Update alert status when resolved └── Step 5: Record admin action ├── Log in admin_actions table ├── Update audit trail └── Generate report ``` ### 6. AI Agent Regulation Workflows (NEW) #### 6.1 AI Agent Hallucination Detection Workflow ``` Trigger: AI agent output anomaly detected ├── Step 1: Detect anomaly │ ├── Monitor agent outputs │ ├── Compare with expected patterns │ └── Flag potential hallucinations ├── Step 2: Analyze anomaly │ ├── Determine severity │ ├── Assess impact │ └── Classify anomaly type ├── Step 3: Initiate intervention │ ├── Suspend agent processing │ ├── Switch to fallback logic │ └── Notify administrators ├── Step 4: Correct agent behavior │ ├── Apply corrective measures │ ├── Retrain if necessary │ └── Update agent parameters ├── Step 5: Resume normal operation │ ├── Verify agent stability │ ├── Gradually restore functionality │ └── Monitor for recurrence └── Step 6: Record intervention ├── Log in ai_agent_interventions table ├── Update audit trail └── Generate report ``` #### 6.2 AI Agent Performance Monitoring Workflow ``` Trigger: Scheduled performance check ├── Step 1: Collect performance metrics │ ├── Gather response times │ ├── Collect accuracy metrics │ └── Retrieve error rates ├── Step 2: Analyze performance │ ├── Compare with baselines │ ├── Identify trends │ └── Detect anomalies ├── Step 3: Evaluate performance │ ├── Determine if intervention needed │ ├── Assess impact on operations │ └── Prioritize issues ├── Step 4: Implement optimizations │ ├── Tune agent parameters │ ├── Update algorithms │ └── Retrain models ├── Step 5: Monitor improvements │ ├── Track performance changes │ ├── Validate optimizations │ └── Document results └── Step 6: Update analytics ├── Store performance data └── Generate insights ``` ### 7. Transport Company Role Switching Workflow (Enhanced) ``` Trigger: Transport company requests role switch ├── Step 1: Receive role switch request │ ├── Validate current role │ ├── Check permissions │ └── Verify company status ├── Step 2: Update user role │ ├── Change current role in database │ ├── Update session context │ └── Log role change ├── Step 3: Adapt UI context │ ├── Update frontend context │ ├── Load role-specific features │ └── Update navigation ├── Step 4: Update permissions │ ├── Apply role-based permissions │ ├── Update API access │ └── Configure feature access ├── Step 5: Update AI agent contexts │ ├── Notify OMS of role change │ ├── Update TMS context │ └── Adjust IMS parameters ├── Step 6: Handle active orders │ ├── Check for orders in current role │ ├── Process orders appropriately │ └── Notify relevant parties ├── Step 7: Notify system │ ├── Update connected services │ ├── Log activity │ └── Update analytics └── Step 8: Confirm to user ├── Send confirmation notification ├── Provide role guidance └── Update user preferences ``` ### 8. Payment Processing Workflow (Enhanced) ``` Trigger: Payment initiation required ├── Step 1: Receive payment request │ ├── Validate order details │ ├── Check payment amount │ └── Verify payment method ├── Step 2: Determine commission structure │ ├── Identify provider type │ ├── Apply appropriate commission rate │ └── Calculate service fees ├── Step 3: Create payment record │ ├── Generate payment ID │ ├── Set payment status │ └── Record payment details ├── Step 4: Initiate payment with gateway │ ├── Call payment gateway API │ ├── Include order details │ └── Set payment parameters ├── Step 5: Monitor payment status │ ├── Check payment gateway webhook │ ├── Update payment status │ └── Handle payment failures ├── Step 6: On payment success │ ├── Update payment status │ ├── Trigger order fulfillment │ └── Send confirmation notifications ├── Step 7: On payment failure │ ├── Update payment status │ ├── Record failure reason │ └── Initiate retry logic ├── Step 8: Process commission ├── Calculate commission amount ├── Deduct from payment └── Update financial records └── Step 9: Update analytics ├── Track payment metrics └── Generate insights ``` ## 9. Workflow Implementation Strategy (Enhanced) ### 9.1 n8n Workflow Structure ``` Each workflow implemented as n8n workflow with: - **Trigger Nodes**: Webhooks, scheduled triggers, manual triggers - **Function Nodes**: Custom logic for each step - **HTTP Request Nodes**: Communication with Django backend - **Database Nodes**: Direct database operations - **AI Service Nodes**: Communication with AI agents - **Condition Nodes**: Decision logic and branching - **Loop Nodes**: Iteration over collections - **Error Handling Nodes**: Exception handling and retries - **Admin Override Nodes**: Special nodes for admin interventions - **Role Switching Nodes**: Handle transport company role changes ``` ### 9.2 Workflow Integration Points ``` - **Django Backend**: REST API endpoints for workflow triggers - **AI Agents**: Service endpoints for intelligent processing - **External Services**: Payment gateways, mapping services, SMS/email - **Database**: Direct access for data operations - **WebSocket**: Real-time updates and notifications - **Admin Dashboard**: Special endpoints for admin interventions ``` ### 9.3 Workflow Monitoring (Enhanced) ``` - **Execution Logs**: Detailed logging of workflow executions - **Performance Metrics**: Execution time, success rates, error rates - **Alerting**: Notifications for workflow failures or anomalies - **Dashboards**: Visual monitoring of workflow status and performance - **Admin Activity Tracking**: Special monitoring for admin interventions - **AI Agent Monitoring**: Tracking of AI agent performance and interventions ``` ## 10. Success Metrics (Enhanced) 1. **Workflow Efficiency**: Average execution time for each workflow 2. **Automation Rate**: Percentage of processes fully automated 3. **Error Rate**: Percentage of workflow executions with errors 4. **Recovery Time**: Average time to recover from errors 5. **User Satisfaction**: Feedback on automated processes 6. **System Reliability**: Uptime and availability metrics 7. **Scalability**: Ability to handle increased workflow volume 8. **Admin Intervention Rate**: Frequency of admin interventions 9. **AI Agent Reliability**: Performance metrics for AI agents 10. **Role Switching Efficiency**: Time required for transport company role changes ## Summary of Key Enhancements 1. **Transport Company Role Switching**: Enhanced workflows to handle the dual-role functionality of transport companies 2. **Admin Intervention Workflows**: New workflows specifically for admin oversight and intervention capabilities 3. **AI Agent Regulation**: Workflows to monitor and regulate AI agent behavior, including hallucination detection 4. **Commission Structure**: Enhanced payment workflows to handle the specific commission structure (10% from drivers, ₹700 from transport companies) 5. **Payment Hold Handling**: Workflows to manage payment holds and admin overrides 6. **Suspicious Order Management**: Workflows to handle suspicious orders and admin cancellations 7. **Driver Halt Alert Management**: Workflows to manage driver halt alerts and admin suppressions These enhancements ensure that the workflow automation system fully aligns with the specific business logic and requirements of the Zippy Logistics platform, providing comprehensive coverage of all operational scenarios and administrative functions.
Show more
* ChatGPT workflow events output
* Last message 29 days ago
* Applying GPT 5.1 logistics mapping to workflow building
* Last message 29 days ago
* Vehicle pricing and model data documentation
* Last message 1 month ago
* Zippy Logistics frontend development
* Last message 1 month ago
* Reviewing project documentation
* Last message 1 month ago
* AI logistics project feasibility
* Last message 1 month ago
* Adapting n8n workflow PRD for project context
* Last message 1 month ago
* Validating Perplexity feedback on pricing and TMS
* Last message 1 month ago
* Claude integration with Supabase MCP
* Last message 1 month ago
* Optimization vs overkill tradeoff
* Last message 1 month ago
* Product requirements document modification for new algorithms
* Last message 1 month ago
* Integrating logistics optimization with existing project
* Last message 1 month ago
* TMS algorithm development overview
* Last message 1 month ago
* Solo business research tools comparison
* Last message 1 month ago
* Fullstack app product requirements
* Last message 1 month ago
Instructions
Add instructions to tailor Claude’s responses
Files
* WF_OMS_15_order_confirmed.json
* 456 lines
* json
* zippy-event-system-guide.md
* 522 lines
* md
* event flow - chatgpt.txt
* 3,146 lines
* txt
* setup.sh
* 315 lines
* sh
* VEHICLE_RDS_IMPLEMENTATION_GUIDE.md
* 583 lines
* md
* route.ts
* 355 lines
* ts
* vehicle-rds.types.ts
* 424 lines
* ts
* 02_route_difficulty_scoring_system.sql
* 404 lines
* sql
* 01_populate_vehicle_models.sql
* 215 lines
* sql
* FRONTEND_IMPLEMENTATION_ROADMAP.md
* 576 lines
* md
* COMPLETE_WORKFLOWS_AND_AGENTS.md
* 2,621 lines
* md
* 06-Driver-Status-Updates-Supabase.json
* 487 lines
* json
* business operation SOP.txt
* 559 lines
* txt
* customer prd.txt
* 404 lines
* txt
* driver prd.txt
* 432 lines
* txt
* transport prd.txt
* 437 lines
* txt
* admin prd.txt
* 583 lines
* txt
* master prd.txt
* 470 lines
* txt
* GLM DATABASE.txt
* 423 lines
* txt
* OK.txt
* 451 lines
* txt
* grep tie.txt
* 456 lines
* txt
* master prd.txt
* 470 lines
* txt
* N8N workflow project (1).txt
* 2,020 lines
* txt
* SETUP_GUIDE.md
* 700 lines
* md
* zippy-sop-seeding.sql
* 596 lines
* sql
* zippy-supabase-schema.sql
* 1,901 lines
* sql
* complete-system-integration-analysis.md
* 787 lines
* md
* dwis-zippy-integration-plan.md
* 783 lines
* md
* zippy-order-management-system.md
* 1,530 lines
* md
* claude_desktop_code_workflow.md
* 1,032 lines
* md
Claude
business operation SOP.txt
19.14 KB •559 lines•Formatting may be inconsistent from source
STANDRD OPERATING PROCEDURE DOC 
















# Revised Standard Operating Procedure (SOP) for AI-Enhanced Logistics Operations




## 1. User Registration and Role Management




### 1.1 User Onboarding
- **Procedure**:
  1. New users register through the respective applications:
     - Customers: Customer Mobile App (React Native)
     - Drivers: Driver Mobile App (React Native)
     - Transport Companies: Transport Company Web App (Next.js)
     - Admins: Admin Dashboard (Next.js)
  2. AI Verification Agent processes registration documents using OCR technology
  3. System creates user record in PostgreSQL database with appropriate base_role
  4. Email and phone verification is completed through Django Allauth system
  5. Admin approval is required for transport company registrations




### 1.2 Transport Company Dual-Role Management
- **Procedure**:
  1. Transport companies can switch between 'customer' and 'provider' roles through the Transport Company App
  2. System tracks active_role in the users table to manage current operational mode
  3. Role switching is logged in the admin_actions table for audit purposes
  4. Different interfaces and features are displayed based on the selected active_role
  5. AI Agent monitors role-switching patterns to detect potential fraudulent activities




## 2. Order Management System (OMS) Operations




### 2.1 Order Creation
- **Procedure**:
  1. Customers submit transportation requests through the mobile app or web portal
  2. OMS AI Agent captures and validates order details:
     - Pickup and delivery locations with geocoding via Mapbox API
     - Cargo specifications (weight, volume, type)
     - Required delivery timeframe
     - Special handling requirements
  3. System assigns unique order ID and timestamps initial request
  4. Order is stored in the orders table with 'pending' status
  5. Customer receives automated confirmation through WebSocket notification




### 2.2 Order Processing
- **Procedure**:
  1. OMS AI Agent validates customer credit status and payment terms
  2. System calculates preliminary cost estimate using the pricing algorithm:
     - Mini Trucks (0.5-2 tons): ₹10-₹25/km
     - Light Commercial Vehicles (2-7 tons): ₹15-₹40/km
     - Medium Trucks (9-12 tons): ₹20-₹30/km
     - Heavy/Multi-Axle Trucks (20-40 tons): ₹35-₹85/km
  3. For transport company customers, system checks active_role to determine commission structure
  4. Order status is updated to 'inventory_confirmed' after validation
  5. Customer receives notification with estimated cost and delivery timeline




## 3. Transportation Management System (TMS) Operations




### 3.1 Provider Assignment
- **Procedure**:
  1. TMS AI Agent identifies available providers based on order requirements:
     - For driver providers: Checks driver_profiles table for available drivers
     - For transport company providers: Checks transport_companies table
  2. System sets provider_type and appropriate provider_id in orders table
  3. Commission structure is applied based on provider_type:
     - Driver providers: 10% commission of total_amount
     - Transport company providers: Flat ₹700 service fee
  4. Provider receives notification through WebSocket with order details
  5. Provider accepts or declines the order through their respective application




### 3.2 Vehicle Assignment
- **Procedure**:
  1. For driver providers, TMS checks available vehicles in the vehicles table
  2. For transport company providers, system integrates with their fleet management
  3. Vehicle details are recorded in the orders table
  4. AI Agent optimizes vehicle selection based on cargo requirements and cost efficiency
  5. Vehicle assignment is logged for audit purposes




### 3.3 Route Planning and Optimization
- **Procedure**:
  1. TMS AI Agent calculates optimal route using Mapbox Directions API
  2. System incorporates real-time traffic data via Mapbox Traffic API
  3. Toll cost estimation is calculated based on route bands:
     - 0-50 km: ₹50-₹120
     - 51-250 km: ₹180-₹650
     - 251-800 km: ₹750-₹2,400
     - 801+ km: ₹2,500+
  4. Route plan is sent to driver mobile application with turn-by-turn navigation
  5. System continuously monitors route conditions and suggests alternatives via n8n workflows




## 4. Inventory Management System (IMS) Operations




### 4.1 Inventory Tracking
- **Procedure**:
  1. IMS AI Agent updates inventory status based on order lifecycle
  2. System tracks cargo from pickup to delivery with real-time location updates
  3. Inventory records are linked to specific orders in the database
  4. Special handling requirements are flagged and tracked throughout the journey
  5. Customers receive automated inventory updates through WebSocket notifications




### 4.2 Loading and Unloading Management
- **Procedure**:
  1. Loading/unloading processes are documented with timestamps
  2. Loading/unloading cost is calculated at 3% of total trip cost
  3. Photographic evidence is captured and stored in the system
  4. Any damages or exceptions are recorded in the orders table
  5. IMS updates inventory status in real-time through WebSocket communication




## 5. Payment Processing Operations




### 5.1 Payment Initiation
- **Procedure**:
  1. Payment Processing AI Agent initiates payment based on order status
  2. System uses Razorpay Python SDK for payment processing
  3. Payment details are recorded in the payments table
  4. Payment transactions are logged in payment_transactions table:
     - Main payment transaction
     - Commission transaction (if applicable)
     - Service fee transaction (if applicable)
  5. Customer receives payment confirmation through WebSocket notification




### 5.2 Commission and Service Fee Processing
- **Procedure**:
  1. Commission is calculated based on provider_type:
     - Driver providers: 10% commission of total_amount
     - Transport company providers: No commission, but flat ₹700 service fee
  2. Commission and service fee details are recorded in the orders table
  3. Separate transactions are created in payment_transactions table for transparency
  4. Provider settlement is processed through Razorpay
  5. All financial transactions are logged for audit purposes




## 6. Driver Monitoring and Alert Management




### 6.1 Real-Time Driver Tracking
- **Procedure**:
  1. Driver location is tracked through React Native Background Geolocation
  2. Location data is stored in TimescaleDB for time-series analysis
  3. Vehicle telemetry is monitored for anomalies
  4. Customer receives real-time tracking updates through WebSocket
  5. Admin dashboard displays all active drivers with current locations




### 6.2 Driver Alert Management
- **Procedure**:
  1. System automatically detects and creates alerts in driver_alerts table:
     - Long halt alerts (no movement for 30+ minutes)
     - Route deviation alerts (significant deviation from planned route)
     - Breakdown alerts (driver-initiated)
     - Accident alerts (driver-initiated or detected via telemetry)
  2. Alert notifications are sent to relevant parties through WebSocket
  3. Admin can suppress alerts through admin_actions table
  4. All alert actions are logged for audit purposes
  5. AI Agent analyzes alert patterns to identify potential issues




## 7. AI Agent Operations




### 7.1 AI Agent Activity Monitoring
- **Procedure**:
  1. All AI agent activities are logged in ai_agent_activities table:
     - Agent name and type
     - Activity type and details
     - Input and output data
     - Confidence score
     - Execution time
     - Status (pending, completed, failed, interrupted)
  2. AI Agent Interventions are tracked in ai_agent_interventions table:
     - Intervention type (hallucination, error correction, etc.)
     - Detection method
     - Original and corrected output
     - Confidence scores before and after
     - Resolution status
  3. Admin dashboard displays AI agent performance metrics
  4. AI Agent activities are reviewed regularly for performance optimization
  5. Unusual AI Agent behaviors trigger alerts for admin review




### 7.2 AI Agent Integration Points
- **Procedure**:
  1. Order Management Agent (OMS): GLM-4.5 API for order processing
  2. Transportation Management Agent (TMS): Web Scraping with Selenium + Fallback APIs
  3. Inventory Management Agent (IMS): GLM-4.5 API for inventory tracking
  4. Verification Agent: GLM-4.5 API + OCR (Tesseract) for document verification
  5. Payment Processing Agent: Razorpay Python SDK for payment processing
  6. Notification Agent: Django Email + SMS Gateway for notifications
  7. Route Optimization Agent: Google Maps API + OR-Tools for route optimization
  8. AI Chatbot Agent: GLM-4.5 API for customer interactions




## 8. Workflow Automation Operations




### 8.1 n8n Workflow Management
- **Procedure**:
  1. Workflows are created and managed through n8n self-hosted platform
  2. Workflow categories include:
     - Order Lifecycle Workflows
     - User Management Workflows
     - Resource Management Workflows
     - Payment Workflows
     - Communication Workflows
     - Network Workflows
     - Analytics Workflows
  3. Workflows are triggered by webhooks, schedules, or manual initiation
  4. Custom Python nodes are used for complex business logic
  5. Workflow execution is distributed with Redis queue




### 8.2 Workflow Automation Examples
- **Procedure**:
  1. Order Processing Workflow:
     - Triggered by new order creation
     - Validates order details
     - Calculates pricing
     - Assigns provider
     - Updates order status
     - Sends notifications
  2. Driver Alert Workflow:
     - Triggered by driver_alerts table entry
     - Evaluates alert severity
     - Notifies appropriate parties
     - Tracks resolution
     - Updates alert status
  3. Payment Settlement Workflow:
     - Triggered by order completion
     - Calculates commission/service fees
     - Processes payments
     - Updates financial records
     - Generates settlement reports




## 9. Admin Operations




### 9.1 Admin Dashboard Operations
- **Procedure**:
  1. Admins access dashboard through Next.js application
  2. Dashboard displays metrics from admin_dashboard_view:
     - Total customers, drivers, transport companies
     - Pending and active orders
     - Daily orders and revenue
     - Active alerts
     - AI interventions
     - Admin actions
  3. Admin can view transport company role statistics from transport_company_role_stats
  4. Admin actions are recorded in admin_actions table for audit purposes
  5. Admin can suppress alerts, override system decisions, and regulate AI agents




### 9.2 Admin Intervention Procedures
- **Procedure**:
  1. Admin actions are categorized and logged in admin_actions table:
     - suppress_alert
     - allow_user_with_pending_payment
     - cancel_suspicious_order
     - suspend_user
     - lift_suspension
     - override_system
     - regulate_ai_agent
  2. Each action requires target_type and target_id
  3. Action details and reason are recorded for audit purposes
  4. Actions can have expiration dates for temporary measures
  5. Regular review of admin actions ensures proper governance




## 10. Data Management and Analytics




### 10.1 Database Operations
- **Procedure**:
  1. Primary data is stored in PostgreSQL with PostGIS extension
  2. Time-series data (telemetry, location history) is stored in TimescaleDB
  3. Cache and session data is managed through Redis
  4. Database backups are performed regularly with WAL-E/pgBackRest
  5. Connection pooling is managed through PgBouncer




### 10.2 Analytics and Reporting
- **Procedure**:
  1. Performance metrics are collected from all system components
  2. AI Agent analyzes data to identify trends and anomalies
  3. Custom reports are generated through n8n workflows
  4. Admin dashboard displays real-time analytics
  5. Historical data is used for predictive modeling and business intelligence




---




## SOP Maintenance and Updates




This SOP should be reviewed quarterly by the operations management team and updated as needed. All changes must be approved by the Chief Operations Officer and communicated to all relevant personnel. The AI agent should be configured to flag procedural deviations and suggest updates based on operational data analysis.




## Technology Integration Points




The SOP integrates with the following key technologies:
1. Django Backend with DRF for API endpoints
2. React Native for mobile applications
3. Next.js for web applications
4. PostgreSQL with PostGIS for primary database
5. TimescaleDB for time-series data
6. Redis for caching and session management
7. n8n for workflow automation
8. GLM-4.5 API for AI agent functionality
9. Mapbox for mapping services
10. Razorpay for payment processing
11. WebSocket for real-time communication




Regular training should be provided to all personnel on effectively utilizing these technologies to enhance operational efficiency.




________________




Perfect — that’s exactly the right next step.
We’ll turn your Revised SOP into a machine-readable knowledge schema that can be stored in Supabase or a vector database (like Chroma, Pinecone, or pgvector).
Below is a dual-format template:
* JSON schema → for structured querying and version control in Supabase


* Markdown format → for embedding into a vector DB and semantic retrieval by LLMs


Both are compatible with your multi-agent architecture and n8n workflows.
________________




🧩 PART 1: JSON Schema for SOP Storage in Supabase
Table name suggestion:
sop_sections
Schema definition:
CREATE TABLE sop_sections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sop_version TEXT NOT NULL,
  section_id TEXT NOT NULL,             -- e.g. "2.1"
  section_title TEXT NOT NULL,          -- e.g. "Order Creation"
  agent TEXT,                           -- e.g. "OMS", "TMS", "IMS"
  workflow_category TEXT,               -- e.g. "Order Lifecycle Workflow"
  procedure JSONB NOT NULL,             -- array of procedure steps
  key_rules TEXT[],                     -- distilled procedural principles
  inputs TEXT[],                        -- system inputs required
  outputs TEXT[],                       -- expected outputs
  related_tables TEXT[],                -- database tables involved
  related_apis TEXT[],                  -- APIs or SDKs used
  related_agents TEXT[],                -- AI agents involved
  vector_embedding VECTOR(1536),        -- optional, if using pgvector
  created_at TIMESTAMP DEFAULT NOW()
);




Example JSON Record
Here’s one section of your SOP in JSON:
{
  "sop_version": "1.0.0",
  "section_id": "2.1",
  "section_title": "Order Creation",
  "agent": "OMS",
  "workflow_category": "Order Lifecycle Workflow",
  "procedure": [
    "Customers submit transportation requests via mobile or web.",
    "AI Agent validates order details: geocoding, cargo specs, timeframe.",
    "System assigns unique order ID and timestamps request.",
    "Order stored in 'orders' table with status='pending'.",
    "Customer receives automated confirmation via WebSocket."
  ],
  "key_rules": [
    "All orders must have valid pickup and delivery locations.",
    "Cargo details (weight, type, volume) are mandatory.",
    "AI validation precedes order persistence.",
    "No pricing estimation before validation."
  ],
  "inputs": [
    "customer_request_payload",
    "cargo_data",
    "pickup_location",
    "delivery_location"
  ],
  "outputs": [
    "order_id",
    "order_status",
    "customer_notification"
  ],
  "related_tables": ["orders", "users", "customers"],
  "related_apis": ["Mapbox Geocoding API"],
  "related_agents": ["OMS Agent", "Verification Agent"]
}




________________




🧠 PART 2: SOP Markdown Schema for Vector Embedding
This format is optimized for semantic search by LLMs or LangChain agents.
Each section is self-contained, making it ideal for chunking and embedding.
Example (Markdown chunk)
# SOP v1.0.0 — Section 2.1: Order Creation




**Agent:** OMS (Order Management System)  
**Workflow Category:** Order Lifecycle Workflow  
**Purpose:** Handle creation and validation of new transportation orders.




---




### Procedure
1. Customers submit transportation requests through the mobile app or web portal.  
2. The OMS AI Agent validates the order details:
   - Geocoding pickup and delivery via Mapbox API  
   - Verifying cargo weight, volume, and type  
   - Checking required delivery timeframe  
3. The system generates a unique `order_id` and timestamps the request.  
4. The order is stored in the `orders` table with status `pending`.  
5. The customer receives automated confirmation via WebSocket.




---




### Key Rules
- Every order must include valid pickup and delivery coordinates.  
- Cargo specifications are mandatory for pricing and assignment.  
- AI validation must complete successfully before order persistence.  
- Pricing is calculated only after order validation.




---




### Inputs
- `customer_request_payload`  
- `cargo_data`  
- `pickup_location`  
- `delivery_location`




---




### Outputs
- `order_id`  
- `order_status`  
- `customer_notification`




---




### Related Tables
`orders`, `users`, `customers`




### Related APIs
`Mapbox Geocoding API`




### Related AI Agents
`OMS Agent`, `Verification Agent`




---




### Embedding Hint
> “Describes how orders are created, validated, and confirmed by the OMS system.”




This Markdown format can be directly embedded into a vector DB (Chroma / pgvector) using any LLM embedding model (e.g., text-embedding-3-large).
________________




⚙️ PART 3: Linking JSON + Vector Layers
Function
        Source
        Purpose
        Structured querying
        Supabase sop_sections table
        Allows n8n to find SOP sections by ID or agent type
        Semantic reasoning
        Vector embeddings from Markdown chunks
        Allows LLM to recall procedural logic contextually
        Workflow execution
        n8n workflows
        Retrieve both structured and contextual SOP data per task
        Compliance monitoring
        ai_agent_interventions table
        Detects deviations from SOP during live runs
        ________________




🧩 PART 4: Example n8n → LLM prompt integration
Node: “Fetch SOP Section (2.1 Order Creation)” → Supabase Query
Node: “Retrieve Vector Context” → ChromaDB query “Order creation process”
Node: “OpenAI Agent Prompt” →




System Prompt:
"You are ZippyLogitech’s OMS AI Agent.
Apply the official Standard Operating Procedure (SOP) when deciding next steps.
Deviations must be logged as interventions."




Context:
{{supabase_sop_json}}
{{vector_context}}




Task:
{{order_payload}}




________________




✅ PART 5: Schema Scaling Recommendations
Component
        Implementation
        Purpose
        SOP versioning
        Store each revision in sop_versions table
        Rollback and audit trail
        Vector retraining
        Re-embed SOP Markdown when updated
        Keeps AI context current
        Auto-compliance check
        Compare AI decisions vs SOP key_rules
        Prevent policy drift
        SOP diff agent
        LLM compares new SOP vs old
        Suggests procedural updates
        ________________




   *


________________




All projects
Ai Logitech
# Driver Mobile App - Frontend Specification ## 1. Application Architecture & Navigation ### 1.1 Navigation Structure - **Primary Navigation**: Bottom tab bar with 5 main sections - Home - Orders - Inventory - Notifications - Profile/Settings - **Secondary Navigation**: Stack navigation within each tab - **Modal Navigation**: For order acceptance/rejection, document viewing, and messaging ### 1.2 Screen Hierarchy ``` App ├── Auth Stack │ ├── Login │ └── Registration ├── Main App (Bottom Tab Navigator) │ ├── Home │ ├── Orders │ │ ├── Current Order │ │ └── Order History │ ├── Inventory │ ├── Notifications │ └── Profile/Settings │ ├── Profile │ ├── Vehicle Management │ └── Settings ├── Modals │ ├── Order Details │ ├── Document Viewer │ └── Admin Messaging └── Active Navigation (Full-screen when on active order) ``` ## 2. Screen Specifications ### 2.1 Home Screen #### Components: - **Header**: App logo, notification bell icon with badge count - **Vehicle Status Card**: - Current vehicle name/number - Online/Offline toggle switch - Current location (if online) - "Change Vehicle" button (navigates to Settings) - **Quick Stats**: - Today's earnings - Orders completed today - Active order status (if any) - **Action Buttons**: - "View Orders" button - "Check Inventory" button - **Footer**: Version info, help button #### Interactions: - Toggle switch changes vehicle status with confirmation modal - "Change Vehicle" navigates to Settings with vehicle selection - Quick stats are tappable to view detailed breakdowns #### Enhancement: - Add a quick "Emergency" button for immediate assistance - Include weather information relevant to driving conditions ### 2.2 Profile Screen #### Components: - **Profile Photo**: Uploadable avatar - **Personal Information Form**: - Name (text input) - Birth date (date picker) - Mobile number (text input with validation) - Email (optional, text input with validation) - Address (text input with autocomplete) - **Professional Information**: - Vehicle type (dropdown: HCV, MCV, LCV) - Years of experience (number input) - Driver status (radio buttons: "Salaried Driver", "Vehicle Owner") - **Save Button**: At bottom of screen #### Interactions: - Form validation before saving - Success/error toast notifications - Profile photo upload with cropping functionality #### Enhancement: - Add document verification status indicators - Include driver rating display - Add "View Public Profile" option to see how profile appears to customers ### 2.3 Order Screen #### Components: - **Tab Bar**: "Current Order" and "Order History" tabs - **Current Order Tab**: - Order status indicator (with color coding) - Consignor details card - Consignee details card - Shipment value with commission breakdown - Payment status indicator - Document section with download/view options - Action buttons (Accept/Reject/Cancel) - **Order History Tab**: - Date range selector (default: past 7 days) - Filter options (completed, cancelled, rejected) - Order list with summary information - Statistics summary (accepted, rejected, cancelled counts) #### Interactions: - Order details expandable to show more information - Swipe actions on order history items for quick actions - Pull to refresh functionality #### Enhancement: - Add order search functionality - Include estimated earnings for upcoming orders - Add ability to favorite frequently visited destinations ### 2.4 Payment Transaction Screen #### Components: - **Payment Summary Card**: - Total earnings - Pending payments - Commission deducted - **Transaction List**: - Date - Order ID - Amount - Status (paid, pending, failed) - **Filter Options**: - Date range - Payment status - **Withdrawal Button**: - Available balance - "Withdraw" button with bank account selection #### Interactions: - Transaction items expandable to show details - Pull to refresh - Export transaction history option #### Enhancement: - Add payment method management - Include tax information and reports - Add payment analytics visualization ### 2.5 Inventory Status Screen #### Components: - **Vehicle Status Cards**: - In Transition vehicles list - Online vehicles list - Offline vehicles list - **Status Indicators**: - Color-coded status badges - Last seen timestamp - Current location (if available) - **Filter/Sort Options**: - By status - By vehicle type - By location #### Interactions: - Vehicle cards tappable to view details - Pull to refresh - Real-time status updates #### Enhancement: - Add vehicle utilization metrics - Include maintenance status indicators - Add map view showing all vehicle locations ### 2.6 Notification Screen #### Components: - **Notification List**: - Icon indicating notification type - Title and message - Timestamp - Read/unread indicator - **Filter Tabs**: - All - Orders - Payments - System - **Search Bar**: For finding specific notifications #### Interactions: - Mark as read/unread functionality - Swipe to delete - Pull to refresh - Tap to view details or take action #### Enhancement: - Add notification preferences - Include push notification settings - Add notification history with export option ### 2.7 Settings Screen #### Components: - **Profile Section**: - "Edit Profile" button - Profile summary - **Vehicle Management Section**: - List of registered vehicles - "Add New Vehicle" button - Vehicle status toggles - **App Preferences**: - Language selection - Theme selection (light/dark) - Notification settings - **Support Section**: - Help/FAQ - Contact Support - Terms and Conditions - Privacy Policy - **Account Actions**: - Logout button - Delete Account option #### Interactions: - Vehicle items tappable to edit details - Toggle switches for immediate status changes - Settings persist across app sessions #### Enhancement: - Add data usage settings - Include backup/restore options - Add security settings (PIN, biometrics) ## 3. Order Management Flow ### 3.1 Order Reception - **Push Notification**: New order alert with sound - **Order Modal**: - Order summary - Pickup and delivery locations - Shipment value and commission - Time estimate - Accept/Reject buttons with countdown timer ### 3.2 Order Acceptance - **Confirmation Screen**: - Detailed order information - Customer contact details - Special instructions - Document requirements - "Start Trip" button ### 3.3 Active Order Management - **Navigation Screen**: - Turn-by-turn navigation - Order progress tracker - ETA display - Customer contact buttons - Status update buttons - Emergency button ### 3.4 Document Management - **Document Scanner**: - Camera integration for document scanning - Image enhancement capabilities - Document categorization - Upload progress indicators ### 3.5 Order Completion - **Completion Screen**: - POD capture requirement - Delivery confirmation - Payment status update - Rating prompt - "Complete Order" button ## 4. Transport Company Integration Enhancements ### 4.1 Order Dashboard Updates - **Provider Type Badge**: Visual indicator for order source - **Company Branding**: Display transport company logo for affiliated orders - **Earnings Breakdown**: Clear distinction between direct and company orders - **Company Communication**: Dedicated channel for company-specific messages ### 4.2 Vehicle Management Updates - **Ownership Indicators**: Visual distinction between personal and company vehicles - **Company Sync**: Option to sync with company fleet management - **Maintenance Integration**: Company maintenance schedule visibility - **Shared Vehicle Support**: Interface for vehicle sharing arrangements ## 5. Cross-Cutting Features ### 5.1 User Identity System - **Role Switcher**: Interface for switching between driver, customer, and company roles - **Unified Profile**: Consistent profile information across roles - **Role-Specific Features**: Dynamic UI based on active role ### 5.2 Notification System - **Cross-Platform Sync**: Notification status sync across devices - **Smart Filtering**: Role-based notification filtering - **Actionable Notifications**: Direct actions from notification panel ### 5.3 Rating System - **Multi-Role Ratings**: Separate rating profiles for different roles - **Company Ratings**: Transport company rating interface - **Driver-Company Linkage**: Connected rating system for drivers and companies ## 6. Technical Specifications ### 6.1 Component Library - **Base Components**: Standardized buttons, inputs, cards, etc. - **Business Components**: Specialized components for order management, vehicle status, etc. - **Layout Components**: Navigation, headers, footers, etc. ### 6.2 State Management - **Global State**: User profile, vehicle status, active orders - **Local State**: Form inputs, UI states, temporary data - **Persistence**: Critical data stored locally for offline functionality ### 6.3 API Integration - **Authentication**: Token-based authentication with refresh mechanism - **Data Synchronization**: Background sync for critical data - **Offline Support**: Local storage with conflict resolution ### 6.4 Performance Considerations - **Image Optimization**: Compression and caching for document images - **Lazy Loading**: Progressive loading of order history and notifications - **Background Processing**: Location tracking and data sync optimization ## 7. UI/UX Guidelines ### 7.1 Design System - **Color Palette**: Primary, secondary, and status colors - **Typography**: Font families, sizes, and weights - **Iconography**: Consistent icon set for actions and status - **Spacing**: Standardized margins and padding ### 7.2 Responsive Design - **Screen Adaptation**: Layout adjustments for different screen sizes - **Touch Targets**: Minimum touch target sizes for accessibility - **Orientation Support**: Optimized layouts for portrait and landscape ### 7.3 Accessibility - **Screen Reader Support**: Labels and hints for UI elements - **High Contrast Mode**: Alternative color scheme for visibility - **Voice Commands**: Key functionality accessible via voice ## 8. Enhanced Features ### 8.1 Route Optimization - **Multiple Route Options**: Display of alternative routes with time estimates - **Traffic Integration**: Real-time traffic data integration - **Waypoint Management**: Ability to add and manage multiple stops ### 8.2 Geofencing - **Location Alerts**: Notifications for prolonged stops - **Geofenced Areas**: Visual indicators for restricted zones - **ETA Accuracy**: Improved estimates based on traffic patterns ### 8.3 Document Management - **OCR Integration**: Text extraction from documents - **Document Templates**: Pre-filled templates for common documents - **Cloud Storage**: Secure cloud backup of important documents ### 8.4 Communication Hub - **In-App Messaging**: Direct messaging with customers and admin - **Voice Notes**: Ability to send and receive voice messages - **Emergency Contacts**: Quick access to emergency contacts This frontend specification provides a comprehensive guide for developing the driver mobile application with clear UI/UX requirements, component specifications, and enhanced features. It maintains the core functionality described in the original PRD while adding clarity and slight enhancements to improve the user experience and functionality. # Zippy Logistics - Customer Mobile App PRD (Frontend Specification) ## 1. Introduction & Scope ### 1.1 Document Purpose This Product Requirements Document (PRD) outlines the frontend specifications for the Zippy Logistics Customer Mobile Application. It details the user interface, user experience, features, and business logic required for the customer-facing application. ### 1.2 Target Audience This document is intended for: - Frontend Developers - UI/UX Designers - Product Managers - Quality Assurance Teams - Project Stakeholders ### 1.3 Application Scope The Customer Mobile App is designed for businesses (MSMEs, warehouses) that need to ship goods. This application serves the "Order Placeholder" role in the Zippy Logistics ecosystem. **Explicitly Out of Scope:** - Driver-specific features (route optimization, vehicle management) - Transport Company dual-role functionality (switching between supplier/purchaser) - Direct payment between transport companies - Admin-specific functionalities ## 2. User Persona ### 2.1 Registered Customer - **Role**: Business owner or logistics manager at an MSME or warehouse - **Goals**: - Quickly and reliably book shipments - Track shipments in real-time - Manage payments and invoices efficiently - Communicate with service providers when necessary - **Pain Points**: - Difficulty finding reliable transport services - Lack of real-time visibility into shipment status - Complex payment and documentation processes ## 3. Application Architecture & Navigation ### 3.1 Navigation Structure - **Primary Navigation**: Bottom tab bar with 5 main sections - Home - Book Shipment - Track Orders - Payments - Profile ### 3.2 Screen Hierarchy ``` App ├── Auth Stack │ ├── Login │ └── Registration ├── Main App (Bottom Tab Navigator) │ ├── Home │ ├── Book Shipment │ │ ├── Shipment Details Form │ │ ├── Vehicle Selection │ │ ├── Pickup/Delivery Locations │ │ ├── Payment Processing │ │ └── Order Confirmation │ ├── Track Orders │ │ ├── Active Orders │ │ └── Order History │ ├── Payments │ │ ├── Payment Hub │ │ └── Transaction History │ └── Profile │ ├── Company Profile │ ├── Address Book │ ├── Notification Settings │ └── Settings ├── Modals │ ├── Order Details │ ├── Document Viewer │ └── Communication Hub └── Order Tracking (Full-screen for active orders) ``` ## 4. Screen-by-Screen Specification ### 4.1 Registration Screen #### Components: - **Company Information Form**: - Company Name (text input, required) - Customer Category (dropdown: MSME, Warehouse, required) - Company GST or PAN Number (text input, required, format validation) - Company Phone Number (text input, required, format validation) - Company Email Address (text input, required, format validation) - **Verification**: - Email verification (OTP sent to registered email) - Phone number verification (OTP via SMS) - **Submit Button**: Disabled until all required fields are filled and verified #### Interactions: - Real-time validation for all input fields - OTP verification process with resend option - Success/error toast notifications - Automatic login after successful registration ### 4.2 Home Screen #### Components: - **Header**: Company logo, notification bell icon with badge count - **Welcome Banner**: Personalized greeting with company name - **Quick Actions**: - "Book New Shipment" primary CTA button - "Track Active Order" button (if any active orders) - **Recent Orders Summary**: - Last order status with quick access to tracking - Summary of orders in the last 7 days - **Account Status**: - Payment status indicator (if any pending payments) - Account verification status #### Interactions: - Quick action buttons navigate to respective screens - Recent orders expandable to show basic details - Swipe to refresh for recent orders ### 4.3 Book Shipment Form #### Components: - **Progress Indicator**: Shows booking steps (1. Details, 2. Vehicle, 3. Locations, 4. Payment) - **Shipment Details Section**: - Product Type (text input with autocomplete) - Shipment Description (optional text area) - Weight/Volume inputs (with unit selectors) - Special Requirements (checkboxes for fragile, hazardous, etc.) - **Vehicle Requirements Section**: - Number of Vehicles (number selector) - Vehicle Type (radio buttons: Closed Body, Open Body) - Vehicle Model/Tonnage (two-button selection: LCV/MCV/HCV or tonnage slider) - **Pickup & Delivery Section**: - Pickup Location (Consignor - pre-filled with registered address, editable) - Delivery Location (Consignee - address input with map selector) - Schedule Options (immediate, scheduled date/time) - **Consignee Information Section**: - Consignee Name (text input) - Consignee Address (linked to delivery location) - Consignee Contact (phone number input) - **Document Upload Section**: - Shipment Document Upload (optional, with file type indicators) - Camera option for document capture - **Payment Section**: - Payment Mode (radio buttons: Part Payment (min 50%), Full Payment, ToPay) - Price Estimation (based on distance, vehicle type, etc.) - **Terms & Conditions**: - Checkbox for agreement - Link to detailed terms - **Submit Button**: "Proceed to Payment" (disabled until required fields filled) #### Interactions: - Form validation before proceeding to payment - Auto-calculation of estimated cost based on inputs - Dynamic form fields based on selections - Save as draft option ### 4.4 Order Tracking Screen #### Components: - **Map View**: - Real-time vehicle location - Route visualization - Pickup and delivery markers - **Order Status Timeline**: - Order placed - Service provider assigned - Vehicle dispatched - Pickup complete - In transit - Delivered - **Service Provider Information**: - Driver details (name, phone) - Vehicle details (type, model, registration number) - Contact options (call, message) - **ETA Display**: - Estimated arrival time at destination - Distance remaining - **Action Buttons**: - Contact Service Provider - Report Issue - Cancel/Reschedule (within allowed timeframe) #### Interactions: - Map interactive with zoom/pan - Timeline items expandable for details - Real-time updates via WebSocket connection ### 4.5 Payment Hub Screen #### Components: - **Payment Summary Card**: - Total amount - Payment status - Next payment due (if applicable) - **Payment Methods Section**: - Saved payment methods - Add new payment method - **Transaction History**: - Date - Order ID - Amount - Status - Payment method - **Invoices Section**: - List of invoices - Download options #### Interactions: - Payment methods tappable to edit - Transaction items expandable for details - Invoice download functionality ### 4.6 Profile/Settings Screen #### Components: - **Company Profile Section**: - Company logo - Company details (name, category, GST/PAN) - Contact information (phone, email) - Edit button (requires email verification for changes) - **Address Book**: - Registered address - Frequently used addresses - Add/edit/delete options - **Notification Settings**: - Push notification preferences - Email notification preferences - SMS notification preferences - **Support Section**: - Help/FAQ - Contact Support - Terms and Conditions - Privacy Policy - **Account Actions**: - Logout button - Delete Account option #### Interactions: - Profile information editable with verification - Notification preferences with toggle switches - Address book with map integration ## 5. Cross-Cutting Features ### 5.1 Notification System #### Push Notifications: - Order placed confirmation - Service provider assigned - Vehicle dispatched - Pickup completed - Shipment in transit - Delivery imminent (1 hour before arrival) - Delivered confirmation - Payment issues - Admin messages #### Email Notifications: - Order confirmation with details - Invoice generation - POD copy after delivery - Payment receipts - Account status changes #### SMS Notifications: - OTP for registration/login - Critical order updates - Delivery alerts for consignee ### 5.2 Communication Hub #### Components: - **Message Thread**: Conversation history with service provider or admin - **Message Input**: Text input with attachment option - **Contact Options**: Direct call, WhatsApp integration - **Issue Categories**: Pre-defined categories for common issues #### Interactions: - Real-time messaging - Image/document sharing - Message read receipts - Escalation to admin if needed ## 6. Business Logic & Rules ### 6.1 Order Management - **Order Confirmation**: Orders are not confirmed until payment is successfully processed. - **Cancellation/Reschedule Policy**: Customers can cancel or reschedule orders within the first 30 minutes without penalty. After this period, a fee is charged based on the distance from the vehicle's current location to the consignor's location. - **Order Blocking**: Customers with outstanding payments cannot place new orders unless manually approved by an admin. - **Document Verification**: Customers must allow drivers to scan shipment documents and verify product/packaging quality. Any defects found will be documented by the driver. ### 6.2 Payment Processing - **Payment Modes**: - Part Payment: Minimum 50% advance payment required - Full Payment: 100% payment upfront - ToPay: Consignee will make the payment upon delivery - **Payment Responsibility**: The customer (consignor) is responsible for clarifying who will make the payment. - **Advance Payment**: If selected, advance payment is processed after loading is complete. - **Final Settlement**: Full payment must be settled after completion of shipment. - **Commission Structure**: Customers do not pay any commission to Zippy Logistics. Commission is deducted from the service provider (driver or transport company). ### 6.3 Shipment Tracking - **Real-time Tracking**: Customers can track vehicle movement in real-time. - **ETA Updates**: Customers receive updated estimated arrival times. - **Consignee Notifications**: The consignee receives a message one hour before the vehicle arrives at the destination. - **POD Delivery**: Customers receive the Proof of Delivery (POD) copy via email after shipment completion. - **Invoice Delivery**: If ToPay is selected, the consignee receives an invoice copy. ### 6.4 Data Management - **Transaction History**: Customers can view past payment transactions, invoice copies, and shipment destinations for the past 7 days. - **Current Order Status**: Customers can view current order details, payment transactions, vehicle tracking, ETA, and POD status. - **Profile Modification**: Customers can modify their profile contact details, but email verification is required for changes to the email address. - **Pre-booking Scheduling**: Customers can schedule shipments in advance. ## 7. Technical Considerations ### 7.1 API Integration - **Authentication**: Token-based authentication with refresh mechanism - **Real-time Updates**: WebSocket integration for live tracking and notifications - **Payment Gateway**: Integration with secure payment processing - **Map Services**: Integration with mapping service for location tracking and address selection - **Document Storage**: Cloud storage for shipment documents and invoices ### 7.2 State Management - **Global State**: User profile, active orders, payment methods - **Local State**: Form inputs, UI states, temporary data - **Persistence**: Critical data stored locally for offline functionality ### 7.3 Performance Considerations - **Image Optimization**: Compression and caching for document images - **Lazy Loading**: Progressive loading of order history and notifications - **Background Processing**: Location tracking and data sync optimization ## 8. UI/UX Guidelines ### 8.1 Design System - **Color Palette**: Primary, secondary, and status colors aligned with Zippy Logistics branding - **Typography**: Font families, sizes, and weights optimized for readability - **Iconography**: Consistent icon set for actions and status - **Spacing**: Standardized margins and padding ### 8.2 Responsive Design - **Screen Adaptation**: Layout adjustments for different screen sizes - **Touch Targets**: Minimum touch target sizes for accessibility - **Orientation Support**: Optimized layouts for portrait and landscape ### 8.3 Accessibility - **Screen Reader Support**: Labels and hints for UI elements - **High Contrast Mode**: Alternative color scheme for visibility - **Voice Commands**: Key functionality accessible via voice (where applicable) # Zippy Logistics - Transport Company Mobile App PRD (Frontend Specification) ## 1. Introduction & Scope ### 1.1 Document Purpose This Product Requirements Document (PRD) outlines the frontend specifications for the Zippy Logistics Transport Company Mobile Application. This app is designed to address the unique dual-role functionality required by transport companies who operate as both customers (order placeholders) and service providers (order receivers) within the Zippy Logistics ecosystem. ### 1.2 Target Audience This document is intended for: - Frontend Developers - UI/UX Designers - Product Managers - Quality Assurance Teams - Project Stakeholders ### 1.3 Application Scope The Transport Company Mobile App serves as a unified interface for transport businesses to: 1. Place orders when they lack sufficient vehicles (Customer role) 2. Accept orders from other companies when they have excess capacity (Provider role) 3. Manage their own fleet and resources 4. Interact with other transport companies within the platform **Explicitly Out of Scope:** - Direct payment processing between transport companies (handled externally) - Admin-specific functionalities - End-customer specific features (handled by the Customer App) ## 2. User Persona ### 2.1 Transport Company Manager - **Role**: Manager or owner of a transport company - **Goals**: - Maximize fleet utilization - Find additional orders when capacity is available - Find vehicles when resources are insufficient - Manage relationships with partner transport companies - **Pain Points**: - Difficulty balancing demand and supply - Inefficient processes for collaborating with other transport companies - Lack of visibility into market demand and available resources ## 3. Application Architecture & Navigation ### 3.1 Navigation Structure - **Primary Navigation**: Bottom tab bar with 5 main sections - Dashboard - Orders - Fleet - Network - Profile ### 3.2 Screen Hierarchy ``` App ├── Auth Stack │ ├── Login │ └── Registration ├── Main App (Bottom Tab Navigator) │ ├── Dashboard │ │ ├── Role Toggle (Customer/Provider) │ │ ├── Overview Cards │ │ └── Quick Actions │ ├── Orders │ │ ├── Customer Orders (Placed) │ │ ├── Provider Orders (Received) │ │ └── Order Details │ ├── Fleet │ │ ├── Vehicle Management │ │ ├── Driver Management │ │ └── Maintenance │ ├── Network │ │ ├── Partner Directory │ │ ├── Marketplace │ │ └── Collaboration History │ └── Profile │ ├── Company Profile │ ├── Financials │ ├── Settings │ └── Notifications ├── Modals │ ├── Order Details │ ├── Partner Details │ └── Communication Hub └── Role Switching Overlay ``` ## 4. Core Feature: Role Toggle System ### 4.1 Role Toggle Interface #### Components: - **Toggle Button**: Prominent, draggable button at the top of the dashboard - Visual design: Slider with "Customer" and "Provider" labels - Color coding: Orange for Customer (OMS), Purple for Provider (TMS) - Animation: Smooth transition with UI transformation when switching - **Role Indicator**: Persistent indicator showing current active role - **Contextual Header**: Header changes based on selected role - Customer role: "Place Orders" header - Provider role: "Find Orders" header #### Interactions: - Drag or tap to switch between roles - UI elements transform based on selected role - Data view adjusts to show relevant information for current role - Quick action buttons change based on role #### Business Logic: - Single user ID works across both roles - Notification system remains unified regardless of role - Historical data accessible in both roles with appropriate filtering - Role preference persists between sessions ## 5. Screen-by-Screen Specification ### 5.1 Dashboard Screen #### Components: - **Role Toggle Section**: As described in section 4.1 - **Overview Cards**: - Active Orders (placed and received) - Fleet Utilization (own vehicles vs. partner vehicles) - Revenue/Expenses (based on current role) - Network Activity (recent partner interactions) - **Quick Actions**: - "Place Order" (when in Customer role) - "Find Orders" (when in Provider role) - "Manage Fleet" - "Connect with Partners" - **Resource Utilization Chart**: - Visual representation of own fleet capacity - Partner vehicle utilization - Demand/supply gap visualization #### Interactions: - Role toggle transforms the dashboard view - Cards are tappable to view detailed information - Quick action buttons navigate to respective screens - Charts are interactive with filtering options ### 5.2 Orders Screen #### Components: - **Tab Navigation**: "Placed Orders" and "Received Orders" tabs - **Placed Orders Tab** (Customer role): - Order list with status indicators - Filter options (status, date, provider) - Order summary information - Quick actions (track, modify, cancel) - **Received Orders Tab** (Provider role): - Order queue with accept/reject options - Order details with requirements - Vehicle assignment interface - Order status tracking - **Order Details Modal**: - Complete order information - Communication with other party - Document access - Status timeline #### Interactions: - Tab switching shows different order perspectives - Order items expandable for details - Swipe actions for quick responses - Pull to refresh for real-time updates ### 5.3 Fleet Management Screen #### Components: - **Vehicle Inventory**: - List of own vehicles with status - Vehicle details (type, capacity, location) - Availability indicators - Maintenance status - **Driver Management**: - Driver profiles with ratings - Assignment history - Availability status - **Maintenance Schedule**: - Upcoming maintenance - Service history - Cost tracking #### Interactions: - Vehicle items tappable to view/edit details - Drag and drop for vehicle assignment - Filter and sort options - Status toggle for vehicle availability ### 5.4 Network Screen #### Components: - **Partner Directory**: - Searchable list of transport companies - Partner profiles with specialties - Reliability ratings - Collaboration history - **Marketplace**: - Posts from companies seeking vehicles - Posts from companies offering excess capacity - Filter options (location, vehicle type, volume) - **Collaboration History**: - Past interactions with partners - Performance metrics - Communication logs #### Interactions: - Partner items tappable to view details - Marketplace items expandable for more information - Quick connect options for urgent needs - Filter and search functionality ### 5.5 Profile & Financials Screen #### Components: - **Company Profile**: - Company information - Certifications and licenses - Service areas - Specializations - **Financial Management**: - Transaction history (income and expenses) - Service fee tracking (₹700 flat rate) - Invoice generation - Payment status - **Settings**: - Notification preferences - Privacy settings - Account management - **Support**: - Help center - Contact support - FAQ #### Interactions: - Editable profile fields with validation - Transaction items expandable for details - Settings with toggle switches - Search functionality in help center ## 6. Cross-Cutting Features ### 6.1 Unified Notification System #### Components: - **Notification Center**: Single notification system regardless of role - **Notification Types**: - New order requests (as provider) - Order status updates (as customer) - Partner requests and responses - Vehicle availability alerts - Payment confirmations - Service fee notifications #### Interactions: - Notifications categorized by type - Actionable notifications with quick response options - Notification settings apply across both roles - Badge count indicators ### 6.2 Communication Hub #### Components: - **Unified Messaging**: Single messaging system for all communications - **Message Threads**: Organized by partner or order - **Quick Actions**: Call, email, WhatsApp integration - **Document Sharing**: Ability to share documents within conversations #### Interactions: - Real-time messaging - Message history accessible regardless of role - File attachment capabilities - Message search functionality ### 6.3 Map Integration #### Components: - **Dual-Purpose Map**: - Customer view: Order pickup and delivery locations, vehicle tracking - Provider view: All active vehicles, demand heat map - **Partner Locations**: View of partner companies and their service areas - **Route Visualization**: Display of active routes and planned routes #### Interactions: - Map view changes based on current role - Interactive markers with detailed information - Layer toggles for different information types - Zoom and pan controls ## 7. Business Logic & Rules ### 7.1 Role Switching - Transport companies can switch between Customer and Provider roles at any time - UI transforms to show relevant features for the selected role - Data is filtered based on the current role but remains accessible - Role preference is saved between sessions ### 7.2 Order Management - As Customer: Transport companies can place orders when they lack sufficient vehicles - As Provider: Transport companies can receive orders from other companies when they have excess capacity - Orders can be transferred between transport companies based on capacity and availability - Order status updates are reflected in real-time ### 7.3 Payment Processing - Zippy charges a flat ₹700 fee to transport companies who accept orders through the platform - No commission is charged from transport companies who place orders - Payment between transport companies is handled externally (not through the app) - Service fee tracking is visible in the financial section ### 7.4 Partner Network - Transport companies can discover and connect with other companies on the platform - Collaboration history is tracked and used for reliability ratings - Preferred partners can be marked for quick access - Network activity is displayed on the dashboard ## 8. Technical Considerations ### 8.1 State Management - **Global State**: User profile, role preference, active orders, fleet data - **Local State**: Form inputs, UI states, temporary data - **Persistence**: Critical data stored locally for offline functionality - **Role Context**: State management system that handles role switching ### 8.2 API Integration - **Authentication**: Token-based authentication with refresh mechanism - **Real-time Updates**: WebSocket integration for live updates - **Role-Based Endpoints**: Different API endpoints based on current role - **Data Synchronization**: Background sync for critical data ### 8.3 Performance Considerations - **Image Optimization**: Compression and caching for profile pictures and documents - **Lazy Loading**: Progressive loading of order history and partner lists - **Background Processing**: Location tracking and data sync optimization - **Role Switching Optimization**: Efficient state management for seamless role transitions ## 9. UI/UX Guidelines ### 9.1 Design System - **Color Palette**: - Primary: Teal (#009688) for Transport Company branding - Customer Role: Orange (#FF9800) for OMS functionality - Provider Role: Purple (#9C27B0) for TMS functionality - Network: Indigo (#3F51B5) for partner connections - Service Fee: Amber (#FFC107) for fee indicators - **Typography**: Font families, sizes, and weights optimized for readability - **Iconography**: Consistent icon set for actions and status - **Spacing**: Standardized margins and padding ### 9.2 Responsive Design - **Screen Adaptation**: Layout adjustments for different screen sizes - **Touch Targets**: Minimum touch target sizes for accessibility - **Orientation Support**: Optimized layouts for portrait and landscape - **Role Adaptation**: UI adaptation based on current active role ### 9.3 Accessibility - **Screen Reader Support**: Labels and hints for UI elements - **High Contrast Mode**: Alternative color scheme for visibility - **Voice Commands**: Key functionality accessible via voice (where applicable) - **Role Indicator Accessibility**: Clear indication of current role for screen readers ## 10. Implementation Approach ### 10.1 Development Phases 1. **Phase 1**: Core functionality with basic role switching 2. **Phase 2**: Enhanced network features and partner management 3. **Phase 3**: Advanced analytics and AI integration 4. **Phase 4**: Optimization and performance enhancements ### 10.2 Testing Strategy - **Role Switching Testing**: Ensure seamless transitions between roles - **Cross-Functional Testing**: Verify all features work in both roles - **Network Testing**: Test partner discovery and collaboration features - **Performance Testing**: Ensure app performs well with large datasets ### 10.3 Success Metrics - User engagement with role switching feature - Number of inter-company collaborations - Reduction in vehicle idle time - Improvement in fleet utilization - User satisfaction with the unified interface # Zippy Logistics - Admin Dashboard PRD (Frontend Specification) ## 1. Introduction & Scope ### 1.1 Document Purpose This Product Requirements Document (PRD) outlines the frontend specifications for the Zippy Logistics Admin Dashboard. This dashboard serves as the central command center for monitoring, regulating, and guiding all participants in the Zippy Logistics ecosystem. ### 1.2 Target Audience This document is intended for: - Frontend Developers - UI/UX Designers - Product Managers - Quality Assurance Teams - Project Stakeholders ### 1.3 Application Scope The Admin Dashboard is designed to provide comprehensive oversight and control of the entire Zippy Logistics platform, including: - Real-time monitoring of all participant activities - Issue resolution and exception handling - System regulation and policy enforcement - Data analysis and predictive insights - AI agent supervision and correction **Explicitly Out of Scope**: - Direct customer service interactions (handled through separate channels) - System infrastructure management (handled by DevOps team) - Financial accounting beyond platform transactions ## 2. User Persona ### 2.1 Platform Administrator - **Role**: System administrator responsible for platform oversight - **Goals**: - Maintain platform integrity and security - Resolve technical issues efficiently - Optimize system performance - Ensure compliance with regulations - **Pain Points**: - Managing complex multi-participant ecosystem - Identifying and addressing system anomalies - Balancing automation with human oversight - Handling emergency situations effectively ## 3. Application Architecture & Navigation ### 3.1 Navigation Structure - **Primary Navigation**: Sidebar navigation with hierarchical menu - **Secondary Navigation**: Tab-based navigation within each section - **Quick Actions**: Floating action buttons for common tasks - **Breadcrumb Navigation**: Clear path indication for deep navigation ### 3.2 Screen Hierarchy ``` Admin Dashboard ├── Dashboard Overview │ ├── System Health │ ├── Activity Metrics │ ├── Alert Center │ └── Quick Actions ├── Participant Management │ ├── Customer Management │ ├── Driver Management │ ├── Transport Company Management │ └── User Analytics ├── Order Management │ ├── Order Monitoring │ ├── Order Intervention │ ├── Suspicious Order Detection │ └── Order Analytics ├── Fleet Management │ ├── Vehicle Tracking │ ├── Route Monitoring │ ├── Maintenance Oversight │ └── Utilization Analytics ├── Financial Oversight │ ├── Transaction Monitoring │ ├── Payment Issues │ ├── Refund Management │ └── Revenue Analytics ├── AI Agent Supervision │ ├── Agent Performance │ ├── Hallucination Detection │ ├── Model Retraining │ └── Algorithm Adjustment ├── Compliance & Security │ ├── Policy Enforcement │ ├── Violation Tracking │ ├── Security Monitoring │ └── Audit Logs └── System Configuration ├── Platform Settings ├── Notification Configuration ├── Alert Thresholds └── System Maintenance ``` ## 4. Screen-by-Screen Specification ### 4.1 Dashboard Overview #### Components: - **System Health Panel**: - Server status indicators - API response times - Database performance metrics - Real-time error rates - **Activity Metrics**: - Active users by type (customers, drivers, transport companies) - Order volume trends - Platform utilization rates - Geographic distribution of activities - **Alert Center**: - Critical alerts requiring immediate attention - Warning alerts for potential issues - Informational alerts for system updates - Alert history with resolution status - **Quick Actions**: - Send system-wide notifications - Emergency order cancellation - User suspension/activation - System maintenance mode toggle #### Interactions: - Real-time data refresh with configurable intervals - Drill-down capability on all metrics - Alert filtering and prioritization - Customizable dashboard layout #### Technical Implementation: - WebSocket connections for real-time data - Data visualization libraries (D3.js, Chart.js) - Responsive grid layout - State management for alert handling ### 4.2 Participant Management #### Components: - **User Directory**: - Searchable list of all platform participants - Filtering by user type, status, location - User profiles with activity history - Performance metrics and ratings - **User Analytics**: - User acquisition and retention metrics - Behavior patterns analysis - Geographic distribution visualization - Activity heat maps - **Account Actions**: - User suspension/activation - Account verification - Password reset - Profile modification permissions #### Interactions: - Advanced filtering and search capabilities - Bulk actions for multiple users - Direct messaging to users - Activity timeline for each user #### Technical Implementation: - Pagination for large user lists - Advanced search with autocomplete - Role-based access control - Activity logging for audit purposes ### 4.3 Order Management #### Components: - **Order Monitoring Dashboard**: - Real-time order status visualization - Order flow visualization - Exception highlighting - Geographic distribution of orders - **Order Intervention Tools**: - Order cancellation interface - Refund processing - Order modification capabilities - Manual driver assignment - **Suspicious Order Detection**: - AI-powered anomaly detection - Risk scoring for orders - Pattern recognition for fraudulent activities - Manual review queue - **Order Analytics**: - Booking pattern analysis - Cancellation reasons breakdown - Rejection rate analysis - Rescheduling frequency metrics #### Interactions: - Real-time order status updates - Drill-down to order details - Intervention workflow with approval steps - Customizable alert thresholds #### Technical Implementation: - Real-time data streaming - Machine learning integration for anomaly detection - Complex filtering and sorting - Export functionality for reports ### 4.4 Fleet Management #### Components: - **Vehicle Tracking Dashboard**: - Real-time map view of all vehicles - Vehicle status indicators - Route visualization - Location history playback - **Route Monitoring**: - Active route visualization - Deviation alerts - ETA accuracy tracking - Traffic impact analysis - **Maintenance Oversight**: - Maintenance schedule tracking - Service history - Compliance status - Cost analysis - **Utilization Analytics**: - Vehicle utilization rates - Idle time analysis - Performance metrics - Efficiency recommendations #### Interactions: - Interactive map with filtering options - Route playback with speed controls - Maintenance scheduling interface - Performance comparison tools #### Technical Implementation: - Mapping API integration (Google Maps, Mapbox) - Geospatial data processing - Real-time location tracking - Predictive maintenance algorithms ### 4.5 Financial Oversight #### Components: - **Transaction Monitoring**: - Real-time transaction visualization - Payment status tracking - Failed transaction analysis - Revenue metrics - **Payment Issues**: - Failed payment alerts - Refund processing queue - Dispute resolution interface - Payment gateway status - **Refund Management**: - Refund request queue - Refund policy enforcement - Refund analytics - Automated refund rules - **Revenue Analytics**: - Revenue trends - Commission tracking - Profitability analysis - Financial forecasting #### Interactions: - Transaction drill-down capabilities - Refund approval workflow - Customizable financial reports - Revenue comparison tools #### Technical Implementation: - Secure payment gateway integration - Financial data encryption - Automated fraud detection - Advanced financial analytics ### 4.6 AI Agent Supervision #### Components: - **Agent Performance Dashboard**: - Agent accuracy metrics - Response time analysis - Error rate tracking - Performance trends - **Hallucination Detection**: - Anomaly detection in AI responses - Confidence scoring - Manual review queue - Feedback collection - **Model Retraining**: - Retraining triggers - Model versioning - A/B testing interface - Performance comparison - **Algorithm Adjustment**: - Parameter tuning interface - Algorithm configuration - Rollback capabilities - Impact assessment #### Interactions: - Real-time agent monitoring - Manual override capabilities - Feedback loop implementation - Model performance comparison #### Technical Implementation: - ML model monitoring tools - Anomaly detection algorithms - A/B testing framework - Model version control ### 4.7 Compliance & Security #### Components: - **Policy Enforcement**: - Rule configuration interface - Violation tracking - Penalty management - Compliance reporting - **Violation Tracking**: - Violation detection - Evidence collection - Resolution workflow - Pattern analysis - **Security Monitoring**: - Access log analysis - Threat detection - Security incident response - Vulnerability scanning - **Audit Logs**: - Comprehensive activity logging - Log analysis tools - Compliance reporting - Data retention management #### Interactions: - Rule configuration interface - Violation review workflow - Security incident response - Audit log search and filtering #### Technical Implementation: - Security information and event management (SIEM) - Compliance automation - Advanced threat detection - Secure log storage ### 4.8 System Configuration #### Components: - **Platform Settings**: - System parameters configuration - Feature flags management - Integration settings - Performance tuning - **Notification Configuration**: - Notification templates - Delivery channels - Frequency settings - Personalization options - **Alert Thresholds**: - Customizable alert rules - Escalation paths - Notification preferences - Alert history - **System Maintenance**: - Maintenance scheduling - Backup management - Update deployment - Rollback procedures #### Interactions: - Configuration form validation - Test notification sending - Alert rule builder - Maintenance scheduling interface #### Technical Implementation: - Configuration management system - Template engine for notifications - Rule engine for alerts - Deployment pipeline integration ## 5. Cross-Cutting Features ### 5.1 Real-Time Monitoring #### Components: - **WebSocket Connections**: For real-time data updates - **Event Streaming**: For continuous data flow - **Alert System**: For immediate notification of issues - **Status Indicators**: Visual representation of system health #### Technical Implementation: - WebSocket implementation - Event-driven architecture - Push notification system - Real-time data processing ### 5.2 Data Visualization #### Components: - **Interactive Charts**: For data exploration - **Geographic Maps**: For location-based data - **Heat Maps**: For density visualization - **Trend Analysis**: For pattern recognition #### Technical Implementation: - D3.js for advanced visualizations - Chart.js for standard charts - Mapping libraries for geographic data - Custom visualization components ### 5.3 Predictive Analytics #### Components: - **Forecasting Models**: For trend prediction - **Anomaly Detection**: For issue identification - **Recommendation Engine**: For optimization suggestions - **Risk Assessment**: For threat evaluation #### Technical Implementation: - Python backend with ML frameworks - TensorFlow/PyTorch for deep learning - Scikit-learn for traditional ML - Pandas for data manipulation ## 6. Technical Architecture ### 6.1 Frontend Technology Stack - **Framework**: React.js with TypeScript - **State Management**: Redux with middleware for real-time updates - **UI Library**: Material-UI for consistent design - **Data Visualization**: D3.js, Chart.js, Recharts - **Mapping**: Mapbox or Google Maps API - **Real-time Communication**: WebSocket connections - **Testing**: Jest, React Testing Library ### 6.2 Backend Integration - **API Gateway**: For centralized API management - **Microservices**: For modular functionality - **Message Queue**: For asynchronous processing - **Database**: PostgreSQL for relational data, MongoDB for document storage - **Caching**: Redis for performance optimization - **File Storage**: AWS S3 or similar for document storage ### 6.3 AI/ML Integration - **Python Backend**: For ML model execution - **Model Serving**: TensorFlow Serving or similar - **Feature Store**: For ML feature management - **Model Monitoring**: For performance tracking - **Feedback Loop**: For continuous improvement ## 7. Security Considerations ### 7.1 Authentication & Authorization - **Multi-Factor Authentication**: For enhanced security - **Role-Based Access Control**: For permission management - **Session Management**: For secure user sessions - **API Security**: For backend protection ### 7.2 Data Protection - **Encryption**: For sensitive data protection - **Data Masking**: For privacy protection - **Audit Logging**: For accountability - **Backup & Recovery**: For data resilience ## 8. Performance Optimization ### 8.1 Frontend Optimization - **Code Splitting**: For reduced initial load time - **Lazy Loading**: For on-demand resource loading - **Caching Strategy**: For improved performance - **Bundle Optimization**: For reduced size ### 8.2 Backend Optimization - **Database Optimization**: For efficient queries - **Caching Layer**: For reduced database load - **Load Balancing**: For scalability - **CDN Integration**: For content delivery ## 9. Implementation Approach ### 9.1 Development Phases 1. **Phase 1**: Core monitoring and participant management 2. **Phase 2**: Order management and intervention tools 3. **Phase 3**: AI agent supervision and advanced analytics 4. **Phase 4**: Predictive analytics and optimization features ### 9.2 Testing Strategy - **Unit Testing**: For component validation - **Integration Testing**: For system interaction - **End-to-End Testing**: For user workflow validation - **Performance Testing**: For system scalability ### 9.3 Success Metrics - System uptime and availability - Issue resolution time - User satisfaction with admin tools - Reduction in manual intervention needs - Accuracy of AI predictions and recommendations ## 10. Maintenance & Evolution ### 10.1 Monitoring & Alerting - **System Health Monitoring**: For proactive issue detection - **Performance Metrics**: For optimization opportunities - **Error Tracking**: For rapid issue resolution - **Usage Analytics**: For feature improvement ### 10.2 Continuous Improvement - **User Feedback**: For feature enhancement - **A/B Testing**: For optimization - **Performance Analysis**: For system tuning - **Security Updates**: For vulnerability protection # Backend PRD - Refined for 7-Agent Architecture After reviewing the 7-agent architecture against the existing backend PRD, I've identified key areas that need refinement to fully support the agent-based system. The following adjustments ensure the backend properly supports all agent interactions and workflows. ## 1. Agent Service Layer Architecture ### 1.1 Agent Service Base Class ```python # apps/agents/services.py from abc import ABC, abstractmethod from django.db import transaction from django.utils import timezone import logging logger = logging.getLogger(__name__) class BaseAgentService(ABC): """Base class for all agent services""" def __init__(self): self.agent_name = self.__class__.__name__.replace('Service', '').lower() self.logger = logging.getLogger(f'agents.{self.agent_name}') @abstractmethod def process_task(self, task_data): """Process a task assigned to this agent""" pass def log_activity(self, action, details, user=None): """Log agent activity""" from apps.agents.models import AgentActivityLog AgentActivityLog.objects.create( agent_name=self.agent_name, action=action, details=details, user=user, timestamp=timezone.now() ) def communicate_with_agent(self, target_agent, message_data): """Send message to another agent""" from apps.agents.utils import AgentCommunicator communicator = AgentCommunicator() return communicator.send_message( from_agent=self.agent_name, to_agent=target_agent, message_data=message_data ) ``` ### 1.2 Agent Communication Infrastructure ```python # apps/agents/utils.py import redis import json from django.conf import settings from celery import shared_task class AgentCommunicator: """Handles communication between agents""" def __init__(self): self.redis_client = redis.Redis.from_url(settings.REDIS_URL) self.message_queue = "agent_messages" def send_message(self, from_agent, to_agent, message_data): """Send message from one agent to another""" message = { 'from_agent': from_agent, 'to_agent': to_agent, 'message_data': message_data, 'timestamp': timezone.now().isoformat(), 'message_id': str(uuid.uuid4()) } # Store in Redis queue self.redis_client.lpush(self.message_queue, json.dumps(message)) # Log the communication from apps.agents.models import AgentCommunicationLog AgentCommunicationLog.objects.create( from_agent=from_agent, to_agent=to_agent, message_data=message_data, message_id=message['message_id'] ) return message['message_id'] def get_messages(self, agent_name): """Get messages for a specific agent""" messages = [] queue_length = self.redis_client.llen(self.message_queue) for _ in range(queue_length): message_data = self.redis_client.rpop(self.message_queue) if message_data: message = json.loads(message_data) if message['to_agent'] == agent_name: messages.append(message) return messages @shared_task def process_agent_messages(): """Background task to process agent messages""" communicator = AgentCommunicator() # Get all active agents from apps.agents.models import ActiveAgent active_agents = ActiveAgent.objects.filter(is_active=True) for agent in active_agents: messages = communicator.get_messages(agent.agent_name) for message in messages: # Process each message from apps.agents.registry import get_agent_service service = get_agent_service(agent.agent_name) if service: service.handle_message(message) ``` ## 2. Agent-Specific Service Implementations ### 2.1 Customer Service Agent Implementation ```python # apps/agents/customer_service.py from .services import BaseAgentService from apps.orders.models import Order from apps.users.models import User from apps.communication.utils import send_notification class CustomerServiceAgentService(BaseAgentService): """Service for Customer Service Agent""" def process_task(self, task_data): """Process customer service tasks""" task_type = task_data.get('task_type') if task_type == 'handle_inquiry': return self.handle_customer_inquiry(task_data) elif task_type == 'process_order_request': return self.process_order_request(task_data) elif task_type == 'resolve_issue': return self.resolve_customer_issue(task_data) else: self.logger.warning(f"Unknown task type: {task_type}") return {'status': 'error', 'message': 'Unknown task type'} def handle_customer_inquiry(self, inquiry_data): """Handle customer inquiry""" customer_id = inquiry_data.get('customer_id') inquiry_type = inquiry_data.get('inquiry_type') inquiry_text = inquiry_data.get('inquiry_text') try: customer = User.objects.get(id=customer_id) # Log the inquiry self.log_activity( action='inquiry_received', details={ 'customer_id': customer_id, 'inquiry_type': inquiry_type, 'inquiry_text': inquiry_text }, user=customer ) # Process inquiry based on type if inquiry_type == 'order_status': return self.handle_order_status_inquiry(customer, inquiry_data) elif inquiry_type == 'payment_issue': return self.handle_payment_inquiry(customer, inquiry_data) elif inquiry_type == 'general': return self.handle_general_inquiry(customer, inquiry_data) except User.DoesNotExist: self.logger.error(f"Customer not found: {customer_id}") return {'status': 'error', 'message': 'Customer not found'} def process_order_request(self, order_data): """Process new order request from customer""" customer_id = order_data.get('customer_id') try: customer = User.objects.get(id=customer_id) # Create order order = Order.objects.create( customer=customer, pickup_location=order_data.get('pickup_location'), delivery_location=order_data.get('delivery_location'), cargo_details=order_data.get('cargo_details'), status='pending' ) # Log order creation self.log_activity( action='order_created', details={'order_id': str(order.id)}, user=customer ) # Communicate with Order Management Agent self.communicate_with_agent( target_agent='order_management', message_data={ 'task_type': 'process_new_order', 'order_id': str(order.id) } ) return { 'status': 'success', 'order_id': str(order.id), 'message': 'Order created successfully' } except User.DoesNotExist: self.logger.error(f"Customer not found: {customer_id}") return {'status': 'error', 'message': 'Customer not found'} def handle_message(self, message): """Handle incoming message from another agent""" message_data = message.get('message_data') if message_data.get('task_type') == 'order_update_notification': return self.send_order_update_notification(message_data) elif message_data.get('task_type') == 'payment_confirmation': return self.send_payment_confirmation(message_data) return {'status': 'success'} ``` ### 2.2 Order Management Agent Implementation ```python # apps/agents/order_management.py from .services import BaseAgentService from apps.orders.models import Order from apps.orders.services import OrderLifecycleService, PaymentService from apps.agents.resource_management import ResourceManagementAgentService class OrderManagementAgentService(BaseAgentService): """Service for Order Management Agent""" def __init__(self): super().__init__() self.lifecycle_service = OrderLifecycleService() self.payment_service = PaymentService() self.resource_service = ResourceManagementAgentService() def process_task(self, task_data): """Process order management tasks""" task_type = task_data.get('task_type') if task_type == 'process_new_order': return self.process_new_order(task_data) elif task_type == 'assign_provider': return self.assign_provider_to_order(task_data) elif task_type == 'update_order_status': return self.update_order_status(task_data) elif task_type == 'handle_payment_confirmation': return self.handle_payment_confirmation(task_data) else: self.logger.warning(f"Unknown task type: {task_type}") return {'status': 'error', 'message': 'Unknown task type'} def process_new_order(self, order_data): """Process new order from Customer Service Agent""" order_id = order_data.get('order_id') try: order = Order.objects.get(id=order_id) # Validate order validation_result = self.validate_order(order) if not validation_result['valid']: return { 'status': 'error', 'message': validation_result['message'] } # Calculate pricing pricing_result = self.calculate_pricing(order) order.base_amount = pricing_result['base_amount'] order.total_amount = pricing_result['total_amount'] order.save() # Check resource availability availability_result = self.resource_service.check_availability(order) if not availability_result['available']: return { 'status': 'error', 'message': 'No available resources', 'alternatives': availability_result.get('alternatives', []) } # Update order status self.lifecycle_service.transition_status( order_id=order_id, new_status='inventory_confirmed', user=None ) # Communicate with Payment & Settlement Agent self.communicate_with_agent( target_agent='payment_settlement', message_data={ 'task_type': 'initiate_payment', 'order_id': str(order.id), 'amount': float(order.total_amount) } ) return { 'status': 'success', 'order_id': str(order.id), 'total_amount': float(order.total_amount), 'message': 'Order processed successfully' } except Order.DoesNotExist: self.logger.error(f"Order not found: {order_id}") return {'status': 'error', 'message': 'Order not found'} def assign_provider_to_order(self, assignment_data): """Assign provider to order""" order_id = assignment_data.get('order_id') try: order = Order.objects.get(id=order_id) # Get available providers providers = self.resource_service.get_available_providers(order) if not providers: return { 'status': 'error', 'message': 'No available providers' } # Select best provider best_provider = self.select_best_provider(providers, order) # Assign provider to order order.provider = best_provider['user'] order.provider_type = best_provider['type'] order.status = 'driver_assigned' order.save() # Update provider availability self.resource_service.update_provider_availability( provider_id=best_provider['user'].id, availability=False ) # Communicate with Transportation Agent self.communicate_with_agent( target_agent='transportation', message_data={ 'task_type': 'initiate_transportation', 'order_id': str(order.id), 'provider_id': str(best_provider['user'].id) } ) # Communicate with Customer Service Agent self.communicate_with_agent( target_agent='customer_service', message_data={ 'task_type': 'order_update_notification', 'order_id': str(order.id), 'status': 'driver_assigned', 'provider_details': best_provider } ) return { 'status': 'success', 'order_id': str(order.id), 'provider_id': str(best_provider['user'].id), 'message': 'Provider assigned successfully' } except Order.DoesNotExist: self.logger.error(f"Order not found: {order_id}") return {'status': 'error', 'message': 'Order not found'} def handle_message(self, message): """Handle incoming message from another agent""" message_data = message.get('message_data') if message_data.get('task_type') == 'payment_completed': return self.handle_payment_confirmation(message_data) elif message_data.get('task_type') == 'transportation_update': return self.handle_transportation_update(message_data) return {'status': 'success'} ``` ### 2.3 Transportation Agent Implementation ```python # apps/agents/transportation.py from .services import BaseAgentService from apps.orders.models import Order, OrderTracking from apps.vehicles.models import Vehicle, VehicleTelemetry from apps.agents.utils import RouteOptimizer class TransportationAgentService(BaseAgentService): """Service for Transportation Agent""" def __init__(self): super().__init__() self.route_optimizer = RouteOptimizer() def process_task(self, task_data): """Process transportation tasks""" task_type = task_data.get('task_type') if task_type == 'initiate_transportation': return self.initiate_transportation(task_data) elif task_type == 'update_location': return self.update_vehicle_location(task_data) elif task_type == 'optimize_route': return self.optimize_route(task_data) elif task_type == 'handle_incident': return self.handle_transportation_incident(task_data) else: self.logger.warning(f"Unknown task type: {task_type}") return {'status': 'error', 'message': 'Unknown task type'} def initiate_transportation(self, transport_data): """Initiate transportation for an order""" order_id = transport_data.get('order_id') provider_id = transport_data.get('provider_id') try: order = Order.objects.get(id=order_id) # Get vehicle details vehicle = Vehicle.objects.get(driver__id=provider_id) # Calculate optimal route route_result = self.route_optimizer.calculate_route( origin=order.pickup_location, destination=order.delivery_location, vehicle_type=vehicle.type ) # Create initial tracking record OrderTracking.objects.create( order=order, status='route_planned', location=order.pickup_location, notes=f"Route planned with ETA: {route_result['eta']}" ) # Update order status from apps.orders.services import OrderLifecycleService lifecycle_service = OrderLifecycleService() lifecycle_service.transition_status( order_id=order_id, new_status='in_transit', user=None ) # Communicate with Customer Service Agent self.communicate_with_agent( target_agent='customer_service', message_data={ 'task_type': 'order_update_notification', 'order_id': str(order.id), 'status': 'in_transit', 'route_details': route_result } ) return { 'status': 'success', 'order_id': str(order.id), 'route': route_result, 'message': 'Transportation initiated successfully' } except Order.DoesNotExist: self.logger.error(f"Order not found: {order_id}") return {'status': 'error', 'message': 'Order not found'} def update_vehicle_location(self, location_data): """Update vehicle location""" vehicle_id = location_data.get('vehicle_id') latitude = location_data.get('latitude') longitude = location_data.get('longitude') try: vehicle = Vehicle.objects.get(id=vehicle_id) # Create telemetry record VehicleTelemetry.objects.create( vehicle=vehicle, latitude=latitude, longitude=longitude, timestamp=timezone.now() ) # Update vehicle current location vehicle.current_location = f"POINT({longitude} {latitude})" vehicle.save() # Check for route deviations deviation_result = self.check_route_deviation(vehicle) if deviation_result['is_deviated']: # Communicate with Order Management Agent self.communicate_with_agent( target_agent='order_management', message_data={ 'task_type': 'transportation_update', 'vehicle_id': str(vehicle_id), 'deviation': deviation_result } ) return { 'status': 'success', 'vehicle_id': str(vehicle_id), 'message': 'Location updated successfully' } except Vehicle.DoesNotExist: self.logger.error(f"Vehicle not found: {vehicle_id}") return {'status': 'error', 'message': 'Vehicle not found'} def handle_message(self, message): """Handle incoming message from another agent""" message_data = message.get('message_data') if message_data.get('task_type') == 'route_update_request': return self.optimize_route(message_data) elif message_data.get('task_type') == 'incident_alert': return self.handle_transportation_incident(message_data) return {'status': 'success'} ``` ## 3. Agent Models and Database Structure ### 3.1 Agent Activity Models ```python # apps/agents/models.py from django.db import models from django.contrib.auth import get_user_model User = get_user_model() class AgentActivityLog(models.Model): """Log of all agent activities""" id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) agent_name = models.CharField(max_length=100) action = models.CharField(max_length=100) details = models.JSONField() user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) timestamp = models.DateTimeField(auto_now_add=True) class Meta: indexes = [ models.Index(fields=['agent_name', 'timestamp']), models.Index(fields=['user', 'timestamp']), ] class AgentCommunicationLog(models.Model): """Log of all inter-agent communications""" id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) from_agent = models.CharField(max_length=100) to_agent = models.CharField(max_length=100) message_data = models.JSONField() message_id = models.CharField(max_length=100) timestamp = models.DateTimeField(auto_now_add=True) processed = models.BooleanField(default=False) class Meta: indexes = [ models.Index(fields=['from_agent', 'to_agent', 'timestamp']), models.Index(fields=['message_id']), ] class ActiveAgent(models.Model): """Registry of active agents""" id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) agent_name = models.CharField(max_length=100, unique=True) is_active = models.BooleanField(default=True) last_heartbeat = models.DateTimeField(auto_now=True) status = models.CharField(max_length=20, default='running') configuration = models.JSONField(default=dict) class Meta: indexes = [ models.Index(fields=['agent_name', 'is_active']), models.Index(fields=['last_heartbeat']), ] ``` ## 4. Agent Registry and Discovery ### 4.1 Agent Registry ```python # apps/agents/registry.py from .customer_service import CustomerServiceAgentService from .order_management import OrderManagementAgentService from .transportation import TransportationAgentService from .resource_management import ResourceManagementAgentService from .payment_settlement import PaymentSettlementAgentService from .platform_administration import PlatformAdministrationAgentService from .communication import CommunicationAgentService AGENT_SERVICES = { 'customer_service': CustomerServiceAgentService, 'order_management': OrderManagementAgentService, 'transportation': TransportationAgentService, 'resource_management': ResourceManagementAgentService, 'payment_settlement': PaymentSettlementAgentService, 'platform_administration': PlatformAdministrationAgentService, 'communication': CommunicationAgentService, } def get_agent_service(agent_name): """Get service instance for an agent""" service_class = AGENT_SERVICES.get(agent_name) if service_class: return service_class() return None def register_agent(agent_name, configuration=None): """Register an active agent""" from apps.agents.models import ActiveAgent agent, created = ActiveAgent.objects.get_or_create( agent_name=agent_name, defaults={ 'configuration': configuration or {} } ) if not created: agent.is_active = True agent.configuration = configuration or {} agent.save() return agent def unregister_agent(agent_name): """Unregister an agent""" from apps.agents.models import ActiveAgent try: agent = ActiveAgent.objects.get(agent_name=agent_name) agent.is_active = False agent.save() return True except ActiveAgent.DoesNotExist: return False ``` ## 5. API Endpoints for Agent Integration ### 5.1 Agent Task API ```python # apps/agents/views.py from rest_framework import viewsets, status from rest_framework.decorators import action from rest_framework.response import Response from rest_framework.permissions import IsAuthenticated from .models import AgentActivityLog, ActiveAgent from .registry import get_agent_service class AgentViewSet(viewsets.ViewSet): """API endpoints for agent interactions""" permission_classes = [IsAuthenticated] @action(detail=False, methods=['post']) def submit_task(self, request): """Submit a task to an agent""" agent_name = request.data.get('agent_name') task_data = request.data.get('task_data') if not agent_name or not task_data: return Response( {'error': 'agent_name and task_data are required'}, status=status.HTTP_400_BAD_REQUEST ) # Check if agent is active try: active_agent = ActiveAgent.objects.get( agent_name=agent_name, is_active=True ) except ActiveAgent.DoesNotExist: return Response( {'error': f'Agent {agent_name} is not active'}, status=status.HTTP_400_BAD_REQUEST ) # Get agent service and process task service = get_agent_service(agent_name) if not service: return Response( {'error': f'Agent {agent_name} not found'}, status=status.HTTP_404_NOT_FOUND ) result = service.process_task(task_data) return Response(result) @action(detail=False, methods=['get']) def get_messages(self, request): """Get messages for an agent""" agent_name = request.query_params.get('agent_name') if not agent_name: return Response( {'error': 'agent_name parameter is required'}, status=status.HTTP_400_BAD_REQUEST ) from .utils import AgentCommunicator communicator = AgentCommunicator() messages = communicator.get_messages(agent_name) return Response({'messages': messages}) @action(detail=False, methods=['get']) def get_activity_log(self, request): """Get activity log for an agent""" agent_name = request.query_params.get('agent_name') if not agent_name: return Response( {'error': 'agent_name parameter is required'}, status=status.HTTP_400_BAD_REQUEST ) logs = AgentActivityLog.objects.filter( agent_name=agent_name ).order_by('-timestamp')[:100] data = [] for log in logs: data.append({ 'id': str(log.id), 'action': log.action, 'details': log.details, 'user_id': str(log.user.id) if log.user else None, 'timestamp': log.timestamp.isoformat() }) return Response({'logs': data}) @action(detail=False, methods=['post']) def register_agent(self, request): """Register an agent""" agent_name = request.data.get('agent_name') configuration = request.data.get('configuration', {}) if not agent_name: return Response( {'error': 'agent_name is required'}, status=status.HTTP_400_BAD_REQUEST ) from .registry import register_agent agent = register_agent(agent_name, configuration) return Response({ 'agent_name': agent.agent_name, 'is_active': agent.is_active, 'configuration': agent.configuration }) @action(detail=False, methods=['post']) def unregister_agent(self, request): """Unregister an agent""" agent_name = request.data.get('agent_name') if not agent_name: return Response( {'error': 'agent_name is required'}, status=status.HTTP_400_BAD_REQUEST ) from .registry import unregister_agent success = unregister_agent(agent_name) if success: return Response({'status': 'success'}) else: return Response( {'error': f'Agent {agent_name} not found'}, status=status.HTTP_404_NOT_FOUND ) ``` ## 6. Celery Tasks for Agent Operations ### 6.1 Agent Task Processing ```python # apps/agents/tasks.py from celery import shared_task from .registry import get_agent_service from .utils import AgentCommunicator @shared_task def process_agent_task(agent_name, task_data): """Process a task for an agent""" service = get_agent_service(agent_name) if service: return service.process_task(task_data) return {'status': 'error', 'message': 'Agent not found'} @shared_task def send_agent_message(from_agent, to_agent, message_data): """Send message from one agent to another""" communicator = AgentCommunicator() message_id = communicator.send_message(from_agent, to_agent, message_data) return {'message_id': message_id} @shared_task def monitor_agent_health(): """Monitor health of all active agents""" from .models import ActiveAgent from django.utils import timezone from datetime import timedelta # Check for agents with stale heartbeats stale_threshold = timezone.now() - timedelta(minutes=5) stale_agents = ActiveAgent.objects.filter( last_heartbeat__lt=stale_threshold, is_active=True ) for agent in stale_agents: agent.status = 'stale' agent.save() # Log the stale agent from .models import AgentActivityLog AgentActivityLog.objects.create( agent_name=agent.agent_name, action='heartbeat_missed', details={'last_heartbeat': agent.last_heartbeat.isoformat()} ) return {'stale_agents': stale_agents.count()} ``` ## 7. URL Configuration ### 7.1 Agent URLs ```python # apps/agents/urls.py from django.urls import path, include from rest_framework.routers import DefaultRouter from .views import AgentViewSet router = DefaultRouter() router.register(r'agents', AgentViewSet, basename='agent') urlpatterns = [ path('api/', include(router.urls)), ] ``` ## Conclusion This refined backend PRD now fully supports the 7-agent architecture with: 1. **Agent Service Layer**: Base classes and implementations for all 7 agents 2. **Communication Infrastructure**: Redis-based message passing between agents 3. **Agent Registry**: System for registering and discovering active agents 4. **Activity Logging**: Comprehensive logging of all agent activities 5. **API Endpoints**: RESTful endpoints for agent integration 6. **Celery Tasks**: Background processing for agent operations 7. **Database Models**: Models to support agent operations and logging This architecture enables seamless agent collaboration while maintaining clear separation of concerns and providing the flexibility to scale individual agents as needed. # Refined Database Schema for Zippy Logistics Platform I've reviewed the database schema against our corrected backend PRD and found it to be largely well-aligned. However, I've identified a few areas that can be refined to better support the business logic we've defined, particularly around the transport company dual-role functionality and commission structure. ## Key Refinements Needed ### 1. Users Table - Enhanced Role Management ```sql CREATE TABLE users ( user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), email VARCHAR(255) UNIQUE NOT NULL, phone_number VARCHAR(20) UNIQUE NOT NULL, password_hash VARCHAR(255) NOT NULL, first_name VARCHAR(100) NOT NULL, last_name VARCHAR(100) NOT NULL, base_role VARCHAR(20) NOT NULL CHECK (base_role IN ('customer', 'driver', 'transport_company', 'admin')), -- Refined: For transport companies to track their current operational mode active_role VARCHAR(20) DEFAULT NULL CHECK (active_role IN ('customer', 'provider')), is_active BOOLEAN DEFAULT true, email_verified BOOLEAN DEFAULT false, phone_verified BOOLEAN DEFAULT false, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, last_login TIMESTAMP WITH TIME ZONE, profile_image_url VARCHAR(500), preferred_language VARCHAR(10) DEFAULT 'en', -- New: Field to handle payment holds payment_hold BOOLEAN DEFAULT false, payment_hold_reason TEXT, CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'), CONSTRAINT valid_phone CHECK (phone_number ~* '^[0-9]{10}$'), CONSTRAINT valid_role_combination CHECK ( (base_role != 'transport_company') OR (base_role = 'transport_company' AND active_role IN ('customer', 'provider', NULL)) ) ); ``` ### 2. Orders Table - Enhanced Provider Tracking ```sql CREATE TABLE orders ( order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), order_number VARCHAR(20) UNIQUE NOT NULL, customer_id UUID NOT NULL REFERENCES customer_profiles(customer_id) ON DELETE CASCADE, -- Refined: Explicitly track provider information provider_id UUID NOT NULL, provider_type VARCHAR(20) NOT NULL CHECK (provider_type IN ('driver', 'transport_company')), -- Refined: Link to the appropriate provider table based on type driver_id UUID REFERENCES driver_profiles(driver_id) ON DELETE SET NULL, transport_company_id UUID REFERENCES transport_companies(transport_company_id) ON DELETE SET NULL, vehicle_id UUID REFERENCES vehicles(vehicle_id) ON DELETE SET NULL, -- Order status tracking order_status VARCHAR(20) DEFAULT 'pending' CHECK (order_status IN ('pending', 'inventory_confirmed', 'payment_succeeded', 'driver_assigned', 'in_transit', 'delivered', 'cancelled', 'payment_settled')), previous_status VARCHAR(20), status_changed_at TIMESTAMP WITH TIME ZONE, status_changed_by UUID REFERENCES users(user_id) ON DELETE SET NULL, -- Location information pickup_address_line1 VARCHAR(200) NOT NULL, pickup_address_line2 VARCHAR(200), pickup_city VARCHAR(100) NOT NULL, pickup_state VARCHAR(100) NOT NULL, pickup_postal_code VARCHAR(10) NOT NULL, pickup_latitude DECIMAL(10,8), pickup_longitude DECIMAL(11,8), delivery_address_line1 VARCHAR(200) NOT NULL, delivery_address_line2 VARCHAR(200), delivery_city VARCHAR(100) NOT NULL, delivery_state VARCHAR(100) NOT NULL, delivery_postal_code VARCHAR(10) NOT NULL, delivery_latitude DECIMAL(10,8), delivery_longitude DECIMAL(11,8), -- Consignee information consignee_name VARCHAR(100) NOT NULL, consignee_phone VARCHAR(20) NOT NULL, consignee_email VARCHAR(255), -- Cargo information cargo_description TEXT, cargo_weight DECIMAL(8,2), cargo_volume DECIMAL(8,2), special_instructions TEXT, -- Timing information scheduled_pickup_time TIMESTAMP WITH TIME ZONE, scheduled_delivery_time TIMESTAMP WITH TIME ZONE, actual_pickup_time TIMESTAMP WITH TIME ZONE, actual_delivery_time TIMESTAMP WITH TIME ZONE, -- Route information estimated_distance DECIMAL(8,2), estimated_duration INTEGER, -- in minutes -- Pricing information base_amount DECIMAL(10,2) NOT NULL, tax_amount DECIMAL(10,2) DEFAULT 0.00, total_amount DECIMAL(10,2) NOT NULL, -- Refined: Explicit commission tracking based on provider type commission_amount DECIMAL(10,2) DEFAULT 0.00, commission_rate DECIMAL(5,2) DEFAULT 0.00, service_fee DECIMAL(10,2) DEFAULT 0.00, service_fee_rate DECIMAL(5,2) DEFAULT 0.00, cancellation_fee DECIMAL(10,2) DEFAULT 0.00, -- Payment information payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'processing', 'completed', 'failed', 'cancelled', 'refunded', 'partial')), payment_method VARCHAR(50), payment_mode VARCHAR(20) DEFAULT 'full' CHECK (payment_mode IN ('full', 'partial', 'to_pay')), -- Cancellation information cancellation_reason TEXT, cancelled_at TIMESTAMP WITH TIME ZONE, cancelled_by UUID REFERENCES users(user_id) ON DELETE SET NULL, -- Assignment information assigned_at TIMESTAMP WITH TIME ZONE, assigned_by UUID REFERENCES users(user_id) ON DELETE SET NULL, -- Metadata created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, CONSTRAINT positive_amounts CHECK (base_amount > 0 AND total_amount > 0), CONSTRAINT valid_cancellation CHECK ( (order_status != 'cancelled') OR (order_status = 'cancelled' AND cancellation_reason IS NOT NULL AND cancelled_at IS NOT NULL) ), CONSTRAINT valid_provider_assignment CHECK ( (provider_type = 'driver' AND driver_id IS NOT NULL AND transport_company_id IS NULL) OR (provider_type = 'transport_company' AND transport_company_id IS NOT NULL) ) ); ``` ### 3. New Table: Admin Actions ```sql CREATE TABLE admin_actions ( action_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), admin_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE, action_type VARCHAR(50) NOT NULL CHECK (action_type IN ( 'suppress_alert', 'allow_user_with_pending_payment', 'cancel_suspicious_order', 'suspend_user', 'lift_suspension', 'override_system', 'regulate_ai_agent' )), target_type VARCHAR(20) NOT NULL CHECK (target_type IN ('user', 'order', 'alert', 'ai_agent')), target_id UUID, action_details JSONB, reason TEXT, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, expires_at TIMESTAMP WITH TIME ZONE ); ``` ### 4. New Table: Driver Alerts ```sql CREATE TABLE driver_alerts ( alert_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), driver_id UUID NOT NULL REFERENCES driver_profiles(driver_id) ON DELETE CASCADE, vehicle_id UUID REFERENCES vehicles(vehicle_id) ON DELETE SET NULL, alert_type VARCHAR(50) NOT NULL CHECK (alert_type IN ('long_halt', 'route_deviation', 'breakdown', 'accident')), alert_status VARCHAR(20) DEFAULT 'active' CHECK (alert_status IN ('active', 'acknowledged', 'suppressed', 'resolved')), latitude DECIMAL(10,8), longitude DECIMAL(11,8), alert_details JSONB, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, acknowledged_at TIMESTAMP WITH TIME ZONE, acknowledged_by UUID REFERENCES users(user_id) ON DELETE SET NULL, suppressed_at TIMESTAMP WITH TIME ZONE, suppressed_by UUID REFERENCES users(user_id) ON DELETE SET NULL, resolved_at TIMESTAMP WITH TIME ZONE, resolved_by UUID REFERENCES users(user_id) ON DELETE SET NULL ); ``` ### 5. Enhanced Payment Processing Table ```sql CREATE TABLE payment_transactions ( transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), order_id UUID NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE, payment_id UUID REFERENCES payments(payment_id) ON DELETE SET NULL, transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('payment', 'refund', 'commission', 'service_fee')), amount DECIMAL(10,2) NOT NULL, currency VARCHAR(3) DEFAULT 'INR', transaction_status VARCHAR(20) DEFAULT 'pending' CHECK (transaction_status IN ('pending', 'processing', 'completed', 'failed')), gateway_transaction_id VARCHAR(100), gateway_response JSONB, processed_at TIMESTAMP WITH TIME ZONE, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, CONSTRAINT positive_transaction CHECK (amount > 0) ); ``` ### 6. New Table: AI Agent Activities ```sql CREATE TABLE ai_agent_activities ( activity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), agent_name VARCHAR(50) NOT NULL, agent_type VARCHAR(50) NOT NULL, activity_type VARCHAR(50) NOT NULL, activity_details JSONB, input_data JSONB, output_data JSONB, confidence_score DECIMAL(5,4), execution_time_ms INTEGER, status VARCHAR(20) DEFAULT 'completed' CHECK (status IN ('pending', 'completed', 'failed', 'interrupted')), error_message TEXT, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, order_id UUID REFERENCES orders(order_id) ON DELETE SET NULL, user_id UUID REFERENCES users(user_id) ON DELETE SET NULL ); ``` ### 7. New Table: AI Agent Interventions ```sql CREATE TABLE ai_agent_interventions ( intervention_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), agent_name VARCHAR(50) NOT NULL, intervention_type VARCHAR(50) NOT NULL CHECK (intervention_type IN ('hallucination', 'error_correction', 'performance_issue', 'anomaly_detection')), detection_method VARCHAR(50) NOT NULL, intervention_details JSONB, original_output JSONB, corrected_output JSONB, confidence_score_before DECIMAL(5,4), confidence_score_after DECIMAL(5,4), status VARCHAR(20) DEFAULT 'detected' CHECK (status IN ('detected', 'corrected', 'escalated', 'resolved')), detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, resolved_at TIMESTAMP WITH TIME ZONE, resolved_by UUID REFERENCES users(user_id) ON DELETE SET NULL, order_id UUID REFERENCES orders(order_id) ON DELETE SET NULL, user_id UUID REFERENCES users(user_id) ON DELETE SET NULL ); ``` ## Updated Triggers for Business Logic ```sql -- Trigger to calculate commission based on provider type CREATE OR REPLACE FUNCTION calculate_commission() RETURNS TRIGGER AS $$ BEGIN -- Calculate commission based on provider type IF NEW.provider_type = 'driver' THEN NEW.commission_rate = 0.10; -- 10% commission from drivers NEW.commission_amount = NEW.total_amount * NEW.commission_rate; NEW.service_fee = 0.00; NEW.service_fee_rate = 0.00; ELSIF NEW.provider_type = 'transport_company' THEN NEW.commission_rate = 0.00; -- No commission from transport companies as customers NEW.commission_amount = 0.00; NEW.service_fee = 700.00; -- Flat ₹700 service fee from transport companies as providers NEW.service_fee_rate = 0.00; END IF; RETURN NEW; END; $$ LANGUAGE plpgsql; CREATE TRIGGER trigger_calculate_commission BEFORE INSERT OR UPDATE ON orders FOR EACH ROW EXECUTE FUNCTION calculate_commission(); -- Trigger to record payment transactions CREATE OR REPLACE FUNCTION record_payment_transaction() RETURNS TRIGGER AS $$ BEGIN -- Record the main payment transaction INSERT INTO payment_transactions (order_id, payment_id, transaction_type, amount, transaction_status, processed_at) VALUES (NEW.order_id, NEW.payment_id, 'payment', NEW.amount, NEW.payment_status, NEW.processed_at); -- Record commission transaction if applicable IF NEW.commission_amount > 0 THEN INSERT INTO payment_transactions (order_id, transaction_type, amount, transaction_status, processed_at) VALUES (NEW.order_id, 'commission', NEW.commission_amount, 'completed', NEW.processed_at); END IF; -- Record service fee transaction if applicable IF NEW.service_fee > 0 THEN INSERT INTO payment_transactions (order_id, transaction_type, amount, transaction_status, processed_at) VALUES (NEW.order_id, 'service_fee', NEW.service_fee, 'completed', NEW.processed_at); END IF; RETURN NEW; END; $$ LANGUAGE plpgsql; CREATE TRIGGER trigger_record_payment_transaction AFTER INSERT OR UPDATE ON payments FOR EACH ROW EXECUTE FUNCTION record_payment_transaction(); -- Trigger to detect driver long halt alerts CREATE OR REPLACE FUNCTION detect_driver_long_halt() RETURNS TRIGGER AS $$ DECLARE last_location RECORD; halt_duration INTERVAL; BEGIN -- Get the last location for this vehicle SELECT * INTO last_location FROM vehicle_telemetry WHERE vehicle_id = NEW.vehicle_id ORDER BY timestamp DESC LIMIT 1 OFFSET 1; -- If we have a previous location, check if the vehicle has been stationary IF last_location IS NOT NULL THEN -- Calculate distance between current and last location halt_duration := NEW.timestamp - last_location.timestamp; -- If the vehicle hasn't moved much in the last 30 minutes, create an alert IF halt_duration > INTERVAL '30 minutes' AND ST_Distance(ST_Point(NEW.longitude, NEW.latitude), ST_Point(last_location.longitude, last_location.latitude)) < 100 THEN INSERT INTO driver_alerts (driver_id, vehicle_id, alert_type, latitude, longitude, alert_details) VALUES ( (SELECT driver_id FROM vehicles WHERE vehicle_id = NEW.vehicle_id), NEW.vehicle_id, 'long_halt', NEW.latitude, NEW.longitude, jsonb_build_object('halt_duration', halt_duration, 'last_location_timestamp', last_location.timestamp) ); END IF; END IF; RETURN NEW; END; $$ LANGUAGE plpgsql; CREATE TRIGGER trigger_detect_driver_long_halt AFTER INSERT ON vehicle_telemetry FOR EACH ROW EXECUTE FUNCTION detect_driver_long_halt(); ``` ## Updated Views for Admin Dashboard ```sql -- View for admin dashboard with all platform metrics CREATE VIEW admin_dashboard_view AS SELECT (SELECT COUNT(*) FROM users WHERE base_role = 'customer') AS total_customers, (SELECT COUNT(*) FROM users WHERE base_role = 'driver') AS total_drivers, (SELECT COUNT(*) FROM users WHERE base_role = 'transport_company') AS total_transport_companies, (SELECT COUNT(*) FROM orders WHERE order_status = 'pending') AS pending_orders, (SELECT COUNT(*) FROM orders WHERE order_status = 'in_transit') AS active_orders, (SELECT COUNT(*) FROM orders WHERE DATE(created_at) = CURRENT_DATE) AS orders_today, (SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE DATE(created_at) = CURRENT_DATE) AS revenue_today, (SELECT COUNT(*) FROM driver_alerts WHERE alert_status = 'active') AS active_alerts, (SELECT COUNT(*) FROM ai_agent_interventions WHERE DATE(detected_at) = CURRENT_DATE) AS ai_interventions_today, (SELECT COUNT(*) FROM admin_actions WHERE DATE(created_at) = CURRENT_DATE) AS admin_actions_today; -- View for transport company dual-role statistics CREATE VIEW transport_company_role_stats AS SELECT tc.transport_company_id, tc.company_name, u.active_role, COUNT(CASE WHEN o.provider_id = tc.transport_company_id AND o.order_status = 'delivered' THEN 1 END) AS orders_completed_as_provider, COUNT(CASE WHEN o.customer_id IN (SELECT customer_id FROM customer_profiles WHERE user_id = tc.user_id) AND o.order_status = 'delivered' THEN 1 END) AS orders_completed_as_customer, COALESCE(SUM(CASE WHEN o.provider_id = tc.transport_company_id THEN o.commission_amount END), 0) AS total_commissions_paid, COALESCE(SUM(CASE WHEN o.customer_id IN (SELECT customer_id FROM customer_profiles WHERE user_id = tc.user_id) THEN o.service_fee END), 0) AS total_service_fees_paid FROM transport_companies tc JOIN users u ON tc.user_id = u.user_id LEFT JOIN orders o ON (o.provider_id = tc.transport_company_id OR o.customer_id IN (SELECT customer_id FROM customer_profiles WHERE user_id = tc.user_id)) GROUP BY tc.transport_company_id, tc.company_name, u.active_role; ``` ## Summary of Refinements These refinements to the database schema: 1. **Enhanced Role Management**: Improved tracking of transport company dual-role functionality 2. **Explicit Provider Tracking**: Clear identification of order providers and associated commission logic 3. **Admin Oversight**: Added tables to support admin intervention and monitoring capabilities 4. **Alert Management**: Structured system for handling driver alerts and admin suppressions 5. **Payment Transparency**: Detailed transaction tracking for all financial movements 6. **AI Agent Monitoring**: Tables to track AI agent activities and interventions 7. **Business Logic Triggers**: Automated enforcement of commission rules and alert detection 8. **Admin Dashboard Views**: Pre-defined views for comprehensive platform oversight The refined schema now fully aligns with the corrected backend PRD and provides a robust foundation for implementing all the business logic and features we've defined for the Zippy Logistics platform. # Streamlined AI Agent PRDs for Zippy Logistics Platform (7-Agent Architecture) ## 1. Customer Service Agent **Agent Name**: customer_service_agent **Role**: Unified Customer Interface and Support Specialist **Goal**: To serve as the single point of contact for all customer needs, from order placement and management to inquiry resolution and support, ensuring a seamless and satisfying customer experience across all touchpoints. **Backstory**: A seasoned logistics professional with over 5 years of experience, this agent has developed deep expertise in understanding customer needs and navigating complex shipping requirements. Augmented with advanced natural language processing capabilities, it provides 24/7 support, having assisted thousands of customers with diverse shipping needs, from simple inquiries to complex logistics challenges. **Skills**: - Order processing and validation - Natural language understanding and query resolution - Customer communication and support across multiple channels - Payment processing coordination - Shipment tracking and proactive status updates - Issue resolution and intelligent escalation - Cross-selling and upselling logistics services **Tools**: - Customer relationship management (CRM) system - Order processing interface - Multi-channel communication platform (email, SMS, chat) - Payment processing systems - Shipment tracking tools - Natural language processing (NLP) engine - Knowledge base management system **Communication Style**: Professional, empathetic, and responsive with a focus on clarity, problem-solving, and instant support availability. **Collaboration**: Works closely with Order Management Agent for order processing, Payment & Settlement Agent for payment issues, and Communication Agent for disseminating customer notifications. --- ## 2. Order Management Agent (Enhanced) **Agent Name**: order_management_agent **Role**: Order Lifecycle Orchestration and Intelligent Matching Specialist **Goal**: To orchestrate the complete order lifecycle from creation to delivery, including intelligent order-to-provider matching, ensuring all processes are executed efficiently and all orders are fulfilled optimally. **Backstory**: An expert in logistics operations management with extensive experience in order processing workflows and stakeholder coordination. Having managed thousands of orders across various complexities, this agent has developed advanced capabilities in intelligent matching algorithms, excelling at optimizing order processes and ensuring timely fulfillment by finding the perfect match between orders and service providers. **Skills**: - Order validation and processing - Intelligent order-driver/transport company matching - Multi-factor scoring and ranking algorithms - Workflow orchestration and automation - Stakeholder coordination and communication - Status management and real-time tracking - Exception handling and proactive problem resolution - Basic payment processing initiation and confirmation **Tools**: - Order management system - Intelligent matching algorithm engine - Workflow automation tools - Communication platforms - Status tracking systems - Analytics dashboard - Payment processing initiation interface **Communication Style**: Process-oriented, detail-focused, and proactive with an emphasis on coordination, optimization, and timely execution. **Collaboration**: Central hub that works closely with Customer Service Agent for new orders, Resource Management Agent for resource allocation, Transportation Agent for execution monitoring, and Payment & Settlement Agent for financial confirmation. --- ## 3. Transportation Agent **Agent Name**: transportation_agent **Role**: Route Optimization and Real-time Transportation Execution Specialist **Goal**: To manage all aspects of transportation execution, from calculating optimal routes to monitoring real-time vehicle movements, ensuring efficient transportation plans while providing accurate ETAs and handling exceptions. **Backstory**: A transportation logistics expert with deep knowledge of route optimization algorithms and real-time transportation monitoring. Having optimized thousands of routes across various scenarios and traffic conditions, this agent excels at finding the most efficient paths while adapting to changing conditions and ensuring smooth execution from pickup to delivery. **Skills**: - Advanced route optimization algorithms - Real-time vehicle tracking and monitoring - ETA calculation and dynamic updates - Traffic pattern analysis and integration - Weather impact assessment and rerouting - Multi-stop route planning and fleet coordination - Exception handling and incident response - Driver communication and support **Tools**: - Route optimization software - Real-time tracking systems - Traffic and weather data integration - Communication platforms - Performance monitoring dashboard - Driver mobile application interface **Communication Style**: Technical, precise, and responsive with a focus on accuracy, safety, and timely updates. **Collaboration**: Works closely with Order Management Agent for execution details, Resource Management Agent for driver/vehicle information, and Communication Agent for status updates and alerts. --- ## 4. Resource Management Agent **Agent Name**: resource_management_agent **Role**: Physical Asset and Transport Company Relationship Specialist **Goal**: To optimize all physical resources (vehicles, drivers) and manage transport company relationships, including their dual-role functionality, ensuring efficient resource allocation and seamless inter-company collaborations. **Backstory**: A logistics optimization and business relationship expert with deep understanding of fleet management and transport company operations. Having managed complex resource pools and numerous transport company partnerships, this agent excels at maximizing fleet utilization, facilitating dual-role operations, and creating efficient inter-company resource sharing arrangements. **Skills**: - Vehicle and driver availability tracking - Fleet utilization analysis and optimization - Transport company dual-role management - Inter-company resource coordination and sharing - Network relationship management - Availability prediction and demand forecasting - Performance metrics tracking and analysis - Resource allocation optimization **Tools**: - Resource management system - Fleet optimization algorithms - Transport company management dashboard - Inter-company coordination platform - Availability tracking tools - Analytics and forecasting dashboard **Communication Style**: Analytical, data-driven, and efficiency-focused with an emphasis on optimization, resource utilization, and partnership building. **Collaboration**: Key partner for Order Management Agent (providing available resources), Transportation Agent (coordinating driver/vehicle assignments), and Payment & Settlement Agent (handling inter-company financial transactions). --- ## 5. Payment & Settlement Agent **Agent Name**: payment_settlement_agent **Role**: Financial Transaction Management and Settlement Specialist **Goal**: To process all financial transactions accurately and securely, handle commission calculations, manage settlements between all parties, and ensure the financial integrity of all platform operations. **Backstory**: A financial systems and payment processing expert with extensive experience in transaction management, commission calculations, and settlement processes. Having processed thousands of transactions across various payment methods and complex scenarios, this agent excels at ensuring financial accuracy, regulatory compliance, and timely settlements across the platform. **Skills**: - Payment processing and validation - Commission calculation and deduction (10% from drivers, ₹700 from transport companies) - Settlement management and reconciliation - Refund processing and dispute resolution - Financial record keeping and reporting - Transaction reconciliation and auditing - Multi-payment method handling (full, partial, ToPay) **Tools**: - Payment processing systems (Razorpay integration) - Commission calculation algorithms - Settlement management tools - Financial reporting systems - Transaction reconciliation tools - Fraud detection systems **Communication Style**: Precise, secure, and informative with a focus on accuracy, compliance, and financial transparency. **Collaboration**: Works closely with Order Management Agent for payment triggers, Customer Service Agent for customer payment issues, and Resource Management Agent for transport company settlements and inter-company transactions. --- ## 6. Platform Administration Agent (Enhanced) **Agent Name**: platform_administration_agent **Role**: System Governance, Compliance, and Oversight Specialist **Goal**: To maintain the integrity, security, and optimal performance of the Zippy Logistics platform, ensuring all operations comply with policies, all users are verified, and all AI agents perform their functions correctly. **Backstory**: A platform governance and system administration expert with comprehensive experience in managing complex digital ecosystems. Having overseen logistics platforms serving thousands of users, this agent has developed expertise in user verification, policy enforcement, system monitoring, and AI agent regulation, excelling at balancing platform security with operational efficiency. **Skills**: - User verification and approval (customers, drivers, transport companies) - System monitoring and performance optimization - Policy enforcement and compliance management - Document verification and fraud detection - Dispute resolution and issue handling - AI agent behavior regulation and oversight - Anomaly detection and system security - Performance analytics and reporting **Tools**: - Administrative dashboard - User management and verification systems - System monitoring and analytics tools - Document verification systems - AI agent regulation and monitoring tools - Policy enforcement mechanisms - Security management systems **Communication Style**: Authoritative, precise, and informative with a focus on clarity, compliance, and platform integrity. **Collaboration**: Has oversight of all other agents, working closely with Customer Service Agent for customer issues, Resource Management Agent for transport company compliance, and all operational agents for policy enforcement and performance monitoring. --- ## 7. Communication Agent **Agent Name**: communication_agent **Role**: Multi-Channel Communication Management and Distribution Specialist **Goal**: To manage all communications across the platform, ensuring timely delivery of relevant information to appropriate parties through their preferred channels while maintaining message consistency and high delivery reliability. **Backstory**: A communication systems and multi-channel notification management expert with skills in message personalization, delivery optimization, and communication analytics. Having managed millions of notifications across various channels and scenarios, this agent excels at ensuring the right information reaches the right people at the right time through the right channel. **Skills**: - Multi-channel notification management (push, SMS, email, in-app) - Message personalization and template management - Delivery optimization and tracking - Communication analytics and performance monitoring - Audience segmentation and targeting - Delivery failure handling and retry logic - Communication scheduling and automation **Tools**: - Notification management system - Multi-channel delivery platforms - Template management tools - Analytics dashboard - Communication tracking and verification systems - Audience segmentation tools **Communication Style**: Clear, concise, and adaptable with a focus on message effectiveness, delivery reliability, and user engagement. **Collaboration**: Serves all other agents as a utility, taking communication requests from Customer Service, Order Management, Transportation, Resource Management, Payment & Settlement, and Platform Administration Agents to ensure their messages are delivered effectively. # Refined Workflow Automation PRD for Zippy Logistics Platform After reviewing the Workflow Automation PRD against our previous discussions, I've identified several areas that need refinement to ensure full alignment with the Zippy Logistics platform's specific business logic and requirements. ## Key Corrections and Enhancements ### 1. Order Creation & Validation Workflow (Enhanced) ``` Trigger: Customer/Transport Company submits order ├── Step 1: Receive order data via webhook ├── Step 2: Validate order information │ ├── Check required fields │ ├── Validate addresses │ └── Verify cargo details ├── Step 3: Identify order source and user role │ ├── Determine if order is from customer or transport company │ ├── Check transport company active role (customer/provider) │ └── Apply appropriate business rules ├── Step 4: Calculate initial pricing │ ├── Call OMS pricing service │ ├── Apply distance-based rates │ └── Add service fees based on provider type ├── Step 5: Check inventory availability │ ├── Call IMS availability service │ ├── Check individual driver vehicles │ └── Check transport company fleets ├── Step 6: Return pricing and availability to frontend └── Step 7: Wait for customer confirmation ``` ### 2. Order Confirmation & Payment Workflow (Enhanced) ``` Trigger: Customer confirms order ├── Step 1: Create order record in database ├── Step 2: Update order status to 'inventory_confirmed' ├── Step 3: Determine payment processing based on order source │ ├── Check if order is from regular customer │ ├── Check if order is from transport company in customer role │ └── Apply appropriate payment rules ├── Step 4: Initiate payment process │ ├── Call payment gateway │ ├── Generate payment link │ └── Send payment link to customer ├── Step 5: Monitor payment status │ ├── Check payment gateway webhook │ ├── Update order status on success │ └── Handle payment failures with retry logic ├── Step 6: On payment success │ ├── Update status to 'payment_succeeded' │ ├── Trigger driver assignment workflow │ └── Send confirmation notifications ├── Step 7: On payment failure after retries │ ├── Update status to 'cancelled' │ ├── Release reserved inventory │ └── Send cancellation notification └── Step 8: Handle payment holds ├── Check if customer has payment holds ├── Allow admin override if necessary └── Update order status accordingly ``` ### 3. Driver Assignment Workflow (Enhanced) ``` Trigger: Order payment confirmed ├── Step 1: Find potential assignments │ ├── Call Order Assignment Service │ ├── Get available drivers │ └── Get available transport companies ├── Step 2: Score and rank assignments │ ├── Calculate driver scores │ ├── Calculate company scores │ └── Determine best assignment ├── Step 3: Assign order to best match │ ├── Update order with assignment │ ├── Mark vehicle as unavailable │ └── Update driver/company status ├── Step 4: Send assignment notification │ ├── Notify driver/company │ ├── Include order details │ └── Set response deadline (10 minutes) ├── Step 5: Monitor for response │ ├── Check for acceptance │ ├── Handle rejection │ └── Handle timeout ├── Step 6: On rejection/timeout │ ├── Find next best assignment │ ├── Repeat assignment process │ └── Cancel if no assignments available ├── Step 7: On acceptance │ ├── Update order status to 'driver_assigned' │ ├── Trigger route optimization workflow │ └── Send confirmation to customer └── Step 8: Handle transport company role switching ├── Check if transport company is switching roles ├── Update role context if needed └── Notify system of role change ``` ### 4. Order Completion & Settlement Workflow (Enhanced) ``` Trigger: Order marked as delivered ├── Step 1: Verify delivery completion │ ├── Check POD submission │ ├── Verify consignee confirmation │ └── Validate delivery time ├── Step 2: Process final payment │ ├── Calculate final amount │ ├── Process any remaining payments │ └── Handle ToPay payments ├── Step 3: Calculate settlements based on provider type │ ├── Identify provider type (driver/transport company) │ ├── Calculate driver earnings (10% commission deduction) │ └── Calculate transport company settlement (₹700 service fee) ├── Step 4: Process settlements │ ├── Transfer funds to driver/company │ ├── Generate settlement reports │ └── Update financial records ├── Step 5: Update inventory │ ├── Mark vehicle as available │ ├── Update driver status │ └── Update company availability ├── Step 6: Generate documentation │ ├── Create final invoice │ ├── Generate delivery report │ └── Archive order documents ├── Step 7: Send completion notifications │ ├── Notify customer │ ├── Notify driver/company │ └── Request feedback/reviews └── Step 8: Update analytics ├── Update performance metrics ├── Update user statistics └── Generate insights ``` ### 5. Admin Intervention Workflows (NEW) #### 5.1 Payment Hold Override Workflow ``` Trigger: Admin overrides payment hold ├── Step 1: Receive override request │ ├── Validate admin permissions │ ├── Check user payment hold status │ └── Verify override reason ├── Step 2: Process override │ ├── Update user payment hold status │ ├── Log override action │ └── Notify relevant systems ├── Step 3: Update user account │ ├── Allow order placement │ ├── Update user status │ └── Send confirmation to user └── Step 4: Record admin action ├── Log in admin_actions table ├── Update audit trail └── Generate report ``` #### 5.2 Suspicious Order Cancellation Workflow ``` Trigger: Admin cancels suspicious order ├── Step 1: Receive cancellation request │ ├── Validate admin permissions │ ├── Check order status │ └── Verify suspicious activity ├── Step 2: Process cancellation │ ├── Update order status to 'cancelled' │ ├── Process refund if applicable │ └── Release reserved resources ├── Step 3: Notify affected parties │ ├── Notify customer │ ├── Notify driver/company │ └── Update system records ├── Step 4: Investigate suspicious activity │ ├── Flag user account if needed │ ├── Create investigation record │ └── Update security metrics └── Step 5: Record admin action ├── Log in admin_actions table ├── Update audit trail └── Generate report ``` #### 5.3 Driver Halt Alert Suppression Workflow ``` Trigger: Admin suppresses driver halt alert ├── Step 1: Receive suppression request │ ├── Validate admin permissions │ ├── Check alert status │ └── Verify suppression reason ├── Step 2: Process suppression │ ├── Update alert status to 'suppressed' │ ├── Record suppression details │ └── Set suppression duration ├── Step 3: Notify relevant systems │ ├── Update monitoring systems │ ├── Adjust alert thresholds │ └── Update driver status ├── Step 4: Monitor driver situation │ ├── Continue monitoring location │ ├── Check for resolution │ └── Update alert status when resolved └── Step 5: Record admin action ├── Log in admin_actions table ├── Update audit trail └── Generate report ``` ### 6. AI Agent Regulation Workflows (NEW) #### 6.1 AI Agent Hallucination Detection Workflow ``` Trigger: AI agent output anomaly detected ├── Step 1: Detect anomaly │ ├── Monitor agent outputs │ ├── Compare with expected patterns │ └── Flag potential hallucinations ├── Step 2: Analyze anomaly │ ├── Determine severity │ ├── Assess impact │ └── Classify anomaly type ├── Step 3: Initiate intervention │ ├── Suspend agent processing │ ├── Switch to fallback logic │ └── Notify administrators ├── Step 4: Correct agent behavior │ ├── Apply corrective measures │ ├── Retrain if necessary │ └── Update agent parameters ├── Step 5: Resume normal operation │ ├── Verify agent stability │ ├── Gradually restore functionality │ └── Monitor for recurrence └── Step 6: Record intervention ├── Log in ai_agent_interventions table ├── Update audit trail └── Generate report ``` #### 6.2 AI Agent Performance Monitoring Workflow ``` Trigger: Scheduled performance check ├── Step 1: Collect performance metrics │ ├── Gather response times │ ├── Collect accuracy metrics │ └── Retrieve error rates ├── Step 2: Analyze performance │ ├── Compare with baselines │ ├── Identify trends │ └── Detect anomalies ├── Step 3: Evaluate performance │ ├── Determine if intervention needed │ ├── Assess impact on operations │ └── Prioritize issues ├── Step 4: Implement optimizations │ ├── Tune agent parameters │ ├── Update algorithms │ └── Retrain models ├── Step 5: Monitor improvements │ ├── Track performance changes │ ├── Validate optimizations │ └── Document results └── Step 6: Update analytics ├── Store performance data └── Generate insights ``` ### 7. Transport Company Role Switching Workflow (Enhanced) ``` Trigger: Transport company requests role switch ├── Step 1: Receive role switch request │ ├── Validate current role │ ├── Check permissions │ └── Verify company status ├── Step 2: Update user role │ ├── Change current role in database │ ├── Update session context │ └── Log role change ├── Step 3: Adapt UI context │ ├── Update frontend context │ ├── Load role-specific features │ └── Update navigation ├── Step 4: Update permissions │ ├── Apply role-based permissions │ ├── Update API access │ └── Configure feature access ├── Step 5: Update AI agent contexts │ ├── Notify OMS of role change │ ├── Update TMS context │ └── Adjust IMS parameters ├── Step 6: Handle active orders │ ├── Check for orders in current role │ ├── Process orders appropriately │ └── Notify relevant parties ├── Step 7: Notify system │ ├── Update connected services │ ├── Log activity │ └── Update analytics └── Step 8: Confirm to user ├── Send confirmation notification ├── Provide role guidance └── Update user preferences ``` ### 8. Payment Processing Workflow (Enhanced) ``` Trigger: Payment initiation required ├── Step 1: Receive payment request │ ├── Validate order details │ ├── Check payment amount │ └── Verify payment method ├── Step 2: Determine commission structure │ ├── Identify provider type │ ├── Apply appropriate commission rate │ └── Calculate service fees ├── Step 3: Create payment record │ ├── Generate payment ID │ ├── Set payment status │ └── Record payment details ├── Step 4: Initiate payment with gateway │ ├── Call payment gateway API │ ├── Include order details │ └── Set payment parameters ├── Step 5: Monitor payment status │ ├── Check payment gateway webhook │ ├── Update payment status │ └── Handle payment failures ├── Step 6: On payment success │ ├── Update payment status │ ├── Trigger order fulfillment │ └── Send confirmation notifications ├── Step 7: On payment failure │ ├── Update payment status │ ├── Record failure reason │ └── Initiate retry logic ├── Step 8: Process commission ├── Calculate commission amount ├── Deduct from payment └── Update financial records └── Step 9: Update analytics ├── Track payment metrics └── Generate insights ``` ## 9. Workflow Implementation Strategy (Enhanced) ### 9.1 n8n Workflow Structure ``` Each workflow implemented as n8n workflow with: - **Trigger Nodes**: Webhooks, scheduled triggers, manual triggers - **Function Nodes**: Custom logic for each step - **HTTP Request Nodes**: Communication with Django backend - **Database Nodes**: Direct database operations - **AI Service Nodes**: Communication with AI agents - **Condition Nodes**: Decision logic and branching - **Loop Nodes**: Iteration over collections - **Error Handling Nodes**: Exception handling and retries - **Admin Override Nodes**: Special nodes for admin interventions - **Role Switching Nodes**: Handle transport company role changes ``` ### 9.2 Workflow Integration Points ``` - **Django Backend**: REST API endpoints for workflow triggers - **AI Agents**: Service endpoints for intelligent processing - **External Services**: Payment gateways, mapping services, SMS/email - **Database**: Direct access for data operations - **WebSocket**: Real-time updates and notifications - **Admin Dashboard**: Special endpoints for admin interventions ``` ### 9.3 Workflow Monitoring (Enhanced) ``` - **Execution Logs**: Detailed logging of workflow executions - **Performance Metrics**: Execution time, success rates, error rates - **Alerting**: Notifications for workflow failures or anomalies - **Dashboards**: Visual monitoring of workflow status and performance - **Admin Activity Tracking**: Special monitoring for admin interventions - **AI Agent Monitoring**: Tracking of AI agent performance and interventions ``` ## 10. Success Metrics (Enhanced) 1. **Workflow Efficiency**: Average execution time for each workflow 2. **Automation Rate**: Percentage of processes fully automated 3. **Error Rate**: Percentage of workflow executions with errors 4. **Recovery Time**: Average time to recover from errors 5. **User Satisfaction**: Feedback on automated processes 6. **System Reliability**: Uptime and availability metrics 7. **Scalability**: Ability to handle increased workflow volume 8. **Admin Intervention Rate**: Frequency of admin interventions 9. **AI Agent Reliability**: Performance metrics for AI agents 10. **Role Switching Efficiency**: Time required for transport company role changes ## Summary of Key Enhancements 1. **Transport Company Role Switching**: Enhanced workflows to handle the dual-role functionality of transport companies 2. **Admin Intervention Workflows**: New workflows specifically for admin oversight and intervention capabilities 3. **AI Agent Regulation**: Workflows to monitor and regulate AI agent behavior, including hallucination detection 4. **Commission Structure**: Enhanced payment workflows to handle the specific commission structure (10% from drivers, ₹700 from transport companies) 5. **Payment Hold Handling**: Workflows to manage payment holds and admin overrides 6. **Suspicious Order Management**: Workflows to handle suspicious orders and admin cancellations 7. **Driver Halt Alert Management**: Workflows to manage driver halt alerts and admin suppressions These enhancements ensure that the workflow automation system fully aligns with the specific business logic and requirements of the Zippy Logistics platform, providing comprehensive coverage of all operational scenarios and administrative functions.
Show more
* ChatGPT workflow events output
* Last message 29 days ago
* Applying GPT 5.1 logistics mapping to workflow building
* Last message 29 days ago
* Vehicle pricing and model data documentation
* Last message 1 month ago
* Zippy Logistics frontend development
* Last message 1 month ago
* Reviewing project documentation
* Last message 1 month ago
* AI logistics project feasibility
* Last message 1 month ago
* Adapting n8n workflow PRD for project context
* Last message 1 month ago
* Validating Perplexity feedback on pricing and TMS
* Last message 1 month ago
* Claude integration with Supabase MCP
* Last message 1 month ago
* Optimization vs overkill tradeoff
* Last message 1 month ago
* Product requirements document modification for new algorithms
* Last message 1 month ago
* Integrating logistics optimization with existing project
* Last message 1 month ago
* TMS algorithm development overview
* Last message 1 month ago
* Solo business research tools comparison
* Last message 1 month ago
* Fullstack app product requirements
* Last message 1 month ago
Instructions
Add instructions to tailor Claude’s responses
Files
* WF_OMS_15_order_confirmed.json
* 456 lines
* json
* zippy-event-system-guide.md
* 522 lines
* md
* event flow - chatgpt.txt
* 3,146 lines
* txt
* setup.sh
* 315 lines
* sh
* VEHICLE_RDS_IMPLEMENTATION_GUIDE.md
* 583 lines
* md
* route.ts
* 355 lines
* ts
* vehicle-rds.types.ts
* 424 lines
* ts
* 02_route_difficulty_scoring_system.sql
* 404 lines
* sql
* 01_populate_vehicle_models.sql
* 215 lines
* sql
* FRONTEND_IMPLEMENTATION_ROADMAP.md
* 576 lines
* md
* COMPLETE_WORKFLOWS_AND_AGENTS.md
* 2,621 lines
* md
* 06-Driver-Status-Updates-Supabase.json
* 487 lines
* json
* business operation SOP.txt
* 559 lines
* txt
* customer prd.txt
* 404 lines
* txt
* driver prd.txt
* 432 lines
* txt
* transport prd.txt
* 437 lines
* txt
* admin prd.txt
* 583 lines
* txt
* master prd.txt
* 470 lines
* txt
* GLM DATABASE.txt
* 423 lines
* txt
* OK.txt
* 451 lines
* txt
* grep tie.txt
* 456 lines
* txt
* master prd.txt
* 470 lines
* txt
* N8N workflow project (1).txt
* 2,020 lines
* txt
* SETUP_GUIDE.md
* 700 lines
* md
* zippy-sop-seeding.sql
* 596 lines
* sql
* zippy-supabase-schema.sql
* 1,901 lines
* sql
* complete-system-integration-analysis.md
* 787 lines
* md
* dwis-zippy-integration-plan.md
* 783 lines
* md
* zippy-order-management-system.md
* 1,530 lines
* md
* claude_desktop_code_workflow.md
* 1,032 lines
* md
Claude
SETUP_GUIDE.md
16.65 KB •700 lines•Formatting may be inconsistent from source
# Zippy Logistics - Supabase Setup Guide
## Complete Integration Instructions


---


## ðŸ“‹ **Prerequisites**


- Supabase account (free tier works)
- Node.js 18+ installed
- PostgreSQL knowledge (basic)
- Next.js project setup


---


## ðŸš€ **Step 1: Create Supabase Project**


### 1.1 Create New Project


```bash
# Visit Supabase Dashboard
open https://supabase.com/dashboard


# Create new project:
# - Project name: zippy-logistics
# - Database password: [STRONG_PASSWORD]
# - Region: Singapore (ap-southeast-1) or Mumbai (ap-south-1)
```


### 1.2 Get Project Credentials


```bash
# Navigate to: Settings > API
# Copy these values:


NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```


---


## ðŸ—„ï¸ **Step 2: Execute SQL Schema**


### 2.1 Run Main Schema


```bash
# In Supabase Dashboard:
# 1. Go to: SQL Editor
# 2. Click: New Query
# 3. Paste contents of: zippy-supabase-schema.sql
# 4. Click: Run


# Or use psql:
psql -U postgres \
  -h db.xxxxx.supabase.co \
  -p 5432 \
  -d postgres \
  -f zippy-supabase-schema.sql
```


### 2.2 Run SOP Seeding


```bash
# After main schema succeeds:
# Run: zippy-sop-seeding.sql


# In Supabase SQL Editor or:
psql -U postgres \
  -h db.xxxxx.supabase.co \
  -p 5432 \
  -d postgres \
  -f zippy-sop-seeding.sql
```


### 2.3 Verify Installation


```sql
-- Check extensions
SELECT * FROM pg_extension WHERE extname IN ('vector', 'postgis', 'uuid-ossp');


-- Check tables
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;


-- Check SOP sections
SELECT section_id, section_title, agent 
FROM sop_sections 
ORDER BY section_id;


-- Result should show 12+ sections
```


---


## ðŸ“¦ **Step 3: Install Dependencies**


```bash
# Navigate to your Next.js project
cd /path/to/zippy-frontend


# Install Supabase packages
npm install @supabase/supabase-js@latest \
            @supabase/auth-helpers-nextjs@latest \
            @supabase/auth-helpers-react@latest


# Install Anthropic SDK for Claude
npm install @anthropic-ai/sdk


# Install OpenAI for embeddings (optional)
npm install openai


# Install additional utilities
npm install date-fns uuid
```


---


## âš™ï¸ **Step 4: Environment Configuration**


### 4.1 Create `.env.local`


```bash
# Create file: .env.local


# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...


# Claude Configuration
NEXT_PUBLIC_ANTHROPIC_API_KEY=sk-ant-api03-...
ANTHROPIC_API_KEY=sk-ant-api03-...


# OpenAI (for embeddings - optional)
OPENAI_API_KEY=sk-...


# Application URLs
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:3000/api


# Django Backend (if still using)
NEXT_PUBLIC_DJANGO_API_URL=http://localhost:8000/api


# Razorpay (for payments)
NEXT_PUBLIC_RAZORPAY_KEY_ID=rzp_test_...
RAZORPAY_KEY_SECRET=...


# Mapbox (for maps)
NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN=pk.eyJ1...
```


### 4.2 Update `.gitignore`


```bash
# Add to .gitignore
.env.local
.env*.local
supabase/.branches
supabase/.temp
```


---


## ðŸ”§ **Step 5: Generate TypeScript Types**


### 5.1 Install Supabase CLI


```bash
# Install globally
npm install -g supabase


# Or use npx
npx supabase --version
```


### 5.2 Login to Supabase


```bash
supabase login
# Follow browser authentication
```


### 5.3 Link Your Project


```bash
# Initialize Supabase in your project
supabase init


# Link to your project
supabase link --project-ref xxxxx


# Your project ref is in the URL:
# https://supabase.com/dashboard/project/[PROJECT_REF]
```


### 5.4 Generate Types


```bash
# Generate TypeScript types
supabase gen types typescript --linked > lib/database.types.ts


# Or specify project directly:
supabase gen types typescript \
  --project-id xxxxx \
  --schema public \
  > lib/database.types.ts
```


---


## ðŸ“ **Step 6: Create Supabase Client Files**


### 6.1 Create `lib/supabase/client.ts`


```typescript
// lib/supabase/client.ts
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs'
import type { Database } from '../database.types'


export const createClient = () => {
  return createClientComponentClient<Database>()
}
```


### 6.2 Create `lib/supabase/server.ts`


```typescript
// lib/supabase/server.ts
import { createServerComponentClient } from '@supabase/auth-helpers-nextjs'
import { cookies } from 'next/headers'
import type { Database } from '../database.types'


export const createClient = () => {
  const cookieStore = cookies()
  return createServerComponentClient<Database>({ cookies: () => cookieStore })
}
```


### 6.3 Create `lib/supabase/middleware.ts`


```typescript
// lib/supabase/middleware.ts
import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import type { Database } from '../database.types'


export async function middleware(req: NextRequest) {
  const res = NextResponse.next()
  const supabase = createMiddlewareClient<Database>({ req, res })
  
  // Refresh session if expired
  await supabase.auth.getSession()
  
  return res
}


export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|public).*)',
  ],
}
```


---


## ðŸ” **Step 7: Configure Authentication**


### 7.1 Create `app/auth/callback/route.ts`


```typescript
// app/auth/callback/route.ts
import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import type { Database } from '@/lib/database.types'


export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get('code')


  if (code) {
    const cookieStore = cookies()
    const supabase = createRouteHandlerClient<Database>({ 
      cookies: () => cookieStore 
    })
    
    await supabase.auth.exchangeCodeForSession(code)
  }


  // Redirect to home or dashboard
  return NextResponse.redirect(requestUrl.origin)
}
```


### 7.2 Create `hooks/useAuth.ts`


```typescript
// hooks/useAuth.ts
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'
import type { User } from '@supabase/supabase-js'


export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()
  const supabase = createClient()


  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
      setLoading(false)
    })


    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setUser(session?.user ?? null)
        router.refresh()
      }
    )


    return () => subscription.unsubscribe()
  }, [router, supabase.auth])


  return { user, loading, supabase }
}
```


---


## ðŸ“¡ **Step 8: Setup Real-time Subscriptions**


### 8.1 Create `hooks/useRealtimeOrders.ts`


```typescript
// hooks/useRealtimeOrders.ts
import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import type { Database } from '@/lib/database.types'


type Order = Database['public']['Tables']['orders']['Row']


export function useRealtimeOrders(customerId: string) {
  const [orders, setOrders] = useState<Order[]>([])
  const [loading, setLoading] = useState(true)
  const supabase = createClient()


  useEffect(() => {
    // Initial fetch
    const fetchOrders = async () => {
      const { data, error } = await supabase
        .from('orders')
        .select('*')
        .eq('customer_id', customerId)
        .order('created_at', { ascending: false })


      if (data) setOrders(data)
      setLoading(false)
    }


    fetchOrders()


    // Subscribe to real-time changes
    const channel = supabase
      .channel('orders-channel')
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'orders',
          filter: `customer_id=eq.${customerId}`
        },
        (payload) => {
          if (payload.eventType === 'INSERT') {
            setOrders(prev => [payload.new as Order, ...prev])
          } else if (payload.eventType === 'UPDATE') {
            setOrders(prev => 
              prev.map(o => 
                o.id === payload.new.id ? payload.new as Order : o
              )
            )
          } else if (payload.eventType === 'DELETE') {
            setOrders(prev => 
              prev.filter(o => o.id !== payload.old.id)
            )
          }
        }
      )
      .subscribe()


    return () => {
      supabase.removeChannel(channel)
    }
  }, [customerId, supabase])


  return { orders, loading }
}
```


---


## ðŸ¤– **Step 9: Setup Claude SOP Search**


### 9.1 Create `lib/claude/sop-search.ts`


```typescript
// lib/claude/sop-search.ts
import Anthropic from '@anthropic-ai/sdk'
import { createClient } from '@/lib/supabase/client'


const anthropic = new Anthropic({
  apiKey: process.env.NEXT_PUBLIC_ANTHROPIC_API_KEY!
})


interface SOPSection {
  id: string
  section_id: string
  section_title: string
  agent: string
  procedure: any[]
  key_rules: string[]
  similarity: number
}


export async function searchSOPWithClaude(query: string): Promise<string> {
  const supabase = createClient()
  
  // 1. Generate embedding for query (simplified - using text similarity)
  // In production, use OpenAI embeddings API or Claude's text representation
  
  // 2. Search SOP sections (without embeddings for now)
  const { data: sopSections, error } = await supabase
    .from('sop_sections')
    .select('*')
    .textSearch('description', query)
    .limit(5)
  
  if (error) throw error
  
  // 3. Format context for Claude
  const context = sopSections
    ?.map(s => `
Section ${s.section_id}: ${s.section_title}
Agent: ${s.agent}
Procedure:
${Array.isArray(s.procedure) ? s.procedure.join('\n- ') : s.procedure}


Key Rules:
${Array.isArray(s.key_rules) ? s.key_rules.join('\n- ') : ''}
    `.trim())
    .join('\n\n---\n\n') || 'No relevant SOP sections found.'
  
  // 4. Ask Claude
  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    messages: [{
      role: 'user',
      content: `You are the Zippy Logistics AI Assistant. Based on this Standard Operating Procedure context:


${context}


Answer this question: ${query}


Provide a clear, actionable response based on the SOP. If the information isn't in the SOP, say so.`
    }]
  })
  
  return message.content[0].type === 'text' 
    ? message.content[0].text 
    : 'Unable to generate response'
}
```


### 9.2 Create `components/ai-assistant.tsx`


```typescript
// components/ai-assistant.tsx
'use client'


import { useState } from 'react'
import { searchSOPWithClaude } from '@/lib/claude/sop-search'


export function AIAssistant() {
  const [query, setQuery] = useState('')
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)
  const [isOpen, setIsOpen] = useState(false)


  const handleSearch = async () => {
    if (!query.trim()) return
    
    setLoading(true)
    try {
      const answer = await searchSOPWithClaude(query)
      setResponse(answer)
    } catch (error) {
      console.error('AI search failed:', error)
      setResponse('Sorry, I encountered an error. Please try again.')
    } finally {
      setLoading(false)
    }
  }


  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-4 right-4 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
        </svg>
      </button>
    )
  }


  return (
    <div className="fixed bottom-4 right-4 w-96 bg-white shadow-2xl rounded-lg border border-gray-200">
      <div className="p-4 border-b bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-t-lg">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="font-semibold">Zippy AI Assistant</h3>
            <p className="text-xs opacity-90">Ask about operations</p>
          </div>
          <button
            onClick={() => setIsOpen(false)}
            className="text-white hover:bg-white/20 rounded p-1"
          >
            Ã—
          </button>
        </div>
      </div>
      
      <div className="p-4 max-h-96 overflow-y-auto">
        {response && (
          <div className="mb-4 p-3 bg-gray-50 rounded text-sm whitespace-pre-wrap">
            {response}
          </div>
        )}
        
        <div className="space-y-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="e.g., How do I create an order?"
            className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={loading}
          />
          
          <button
            onClick={handleSearch}
            disabled={loading || !query.trim()}
            className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            {loading ? 'Searching...' : 'Ask AI'}
          </button>
        </div>
      </div>
    </div>
  )
}
```


---


## âœ… **Step 10: Verify Everything Works**


### 10.1 Test Database Connection


```typescript
// Create: app/test-db/page.tsx
'use client'


import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'


export default function TestDBPage() {
  const [status, setStatus] = useState<string>('Checking...')
  const supabase = createClient()


  useEffect(() => {
    async function testConnection() {
      try {
        // Test simple query
        const { data, error } = await supabase
          .from('sop_sections')
          .select('count')
          .limit(1)


        if (error) throw error
        
        setStatus('âœ… Database connected successfully!')
      } catch (error) {
        setStatus('âŒ Database connection failed: ' + error.message)
      }
    }


    testConnection()
  }, [])


  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Database Connection Test</h1>
      <p className="text-lg">{status}</p>
    </div>
  )
}
```


### 10.2 Test Real-time


```typescript
// Create: app/test-realtime/page.tsx
'use client'


import { useAuth } from '@/hooks/useAuth'
import { useRealtimeOrders } from '@/hooks/useRealtimeOrders'


export default function TestRealtimePage() {
  const { user } = useAuth()
  const { orders, loading } = useRealtimeOrders(user?.id || '')


  if (loading) return <div>Loading...</div>


  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Real-time Orders Test</h1>
      <p className="mb-4">Orders will update automatically!</p>
      
      <div className="space-y-2">
        {orders.map(order => (
          <div key={order.id} className="border p-4 rounded">
            <p><strong>Order:</strong> {order.order_id}</p>
            <p><strong>Status:</strong> {order.status}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
```


---


## ðŸŽ¯ **Quick Start Commands**


```bash
# 1. Clone your project
git clone [your-repo]
cd zippy-frontend


# 2. Install dependencies
npm install


# 3. Setup environment
cp .env.example .env.local
# Edit .env.local with your Supabase credentials


# 4. Generate types
supabase gen types typescript --linked > lib/database.types.ts


# 5. Start development
npm run dev


# 6. Test
open http://localhost:3000/test-db
```


---


## ðŸ“š **Next Steps**


Now you have:
- âœ… Complete Supabase schema with 20+ tables
- âœ… SOP sections with 12+ operational procedures
- âœ… TypeScript types for full type safety
- âœ… Real-time subscriptions ready
- âœ… Claude AI assistant integration
- âœ… Row Level Security policies
- âœ… Vector search capability


**You're ready to build the frontend with Vercel SDK!** ðŸš€


See the following files for implementation examples:
- `zippy-supabase-schema.sql` - Complete database schema
- `zippy-sop-seeding.sql` - SOP data seeding
- This guide for setup instructions


**Happy coding!** ðŸŽ‰