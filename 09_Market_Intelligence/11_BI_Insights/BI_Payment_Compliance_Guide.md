# Payment & Compliance Guide

> **Razorpay Integration, GST Compliance, and Indian Logistics Regulations**

---

## 1. Executive Summary

| Component | Solution | Priority |
|-----------|----------|----------|
| **Payment Gateway** | Razorpay (Primary) + Cashfree (Backup) | P0 |
| **GST Invoicing** | GSP-integrated invoicing | P0 |
| **E-Way Bill** | NIC API Integration | P0 |
| **Insurance** | ICICI Lombard / Bajaj Alliance | P1 |
| **KYC Verification** | Karza / Digio | P1 |

---

## 2. Payment Gateway Architecture

### 2.1 Razorpay Integration

#### 2.1.1 Backend Configuration (FastAPI)

```python
# services/payment/razorpay_service.py
import razorpay
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional
import hmac
import hashlib
import os

class RazorpayConfig:
    KEY_ID = os.getenv("RAZORPAY_KEY_ID")
    KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
    WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET")
    
class PaymentOrderRequest(BaseModel):
    amount: int  # in paise (₹184.08 = 18408)
    currency: str = "INR"
    receipt: str  # Booking ID
    notes: dict = {}
    
class PaymentService:
    def __init__(self):
        self.client = razorpay.Client(
            auth=(RazorpayConfig.KEY_ID, RazorpayConfig.KEY_SECRET)
        )
    
    async def create_order(self, request: PaymentOrderRequest) -> dict:
        """Create Razorpay order for a booking"""
        try:
            order_data = {
                "amount": request.amount,
                "currency": request.currency,
                "receipt": request.receipt,
                "notes": request.notes,
                "payment_capture": 1  # Auto-capture
            }
            
            order = self.client.order.create(data=order_data)
            
            # Store order in database
            await self._save_order_to_db(order, request.receipt)
            
            return {
                "order_id": order["id"],
                "amount": order["amount"],
                "currency": order["currency"],
                "key_id": RazorpayConfig.KEY_ID,
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Order creation failed: {str(e)}")
    
    async def verify_payment(self, order_id: str, payment_id: str, signature: str) -> bool:
        """Verify payment signature"""
        try:
            generated_signature = hmac.new(
                RazorpayConfig.KEY_SECRET.encode(),
                f"{order_id}|{payment_id}".encode(),
                hashlib.sha256
            ).hexdigest()
            
            is_valid = generated_signature == signature
            
            if is_valid:
                # Update booking status
                await self._confirm_payment(order_id, payment_id)
                
            return is_valid
        except Exception as e:
            return False
    
    async def process_refund(self, payment_id: str, amount: int, reason: str) -> dict:
        """Process refund"""
        try:
            refund_data = {
                "amount": amount,
                "speed": "normal",  # or "optimum" for instant
                "notes": {
                    "reason": reason,
                    "booking_id": "..."
                }
            }
            
            refund = self.client.payment.refund(payment_id, refund_data)
            await self._log_refund(refund)
            
            return refund
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Refund failed: {str(e)}")
    
    async def handle_webhook(self, payload: bytes, signature: str) -> dict:
        """Process Razorpay webhook events"""
        # Verify webhook signature
        expected_signature = hmac.new(
            RazorpayConfig.WEBHOOK_SECRET.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(expected_signature, signature):
            raise HTTPException(status_code=400, detail="Invalid webhook signature")
        
        event = json.loads(payload)
        
        # Handle different event types
        handlers = {
            "payment.captured": self._handle_payment_captured,
            "payment.failed": self._handle_payment_failed,
            "refund.processed": self._handle_refund_processed,
            "order.paid": self._handle_order_paid,
        }
        
        handler = handlers.get(event["event"])
        if handler:
            await handler(event["payload"])
        
        return {"status": "processed"}
```

#### 2.1.2 Frontend Integration (React)

```typescript
// hooks/useRazorpay.ts
import { useCallback } from 'react';

interface RazorpayOptions {
  key: string;
  amount: number;
  currency: string;
  name: string;
  description: string;
  order_id: string;
  prefill: {
    name: string;
    email: string;
    contact: string;
  };
  notes: {
    booking_id: string;
  };
  theme: {
    color: '#2563eb';
  };
  handler: (response: RazorpayResponse) => void;
}

interface RazorpayResponse {
  razorpay_payment_id: string;
  razorpay_order_id: string;
  razorpay_signature: string;
}

export function useRazorpay() {
  const loadScript = useCallback(() => {
    return new Promise((resolve) => {
      const script = document.createElement('script');
      script.src = 'https://checkout.razorpay.com/v1/checkout.js';
      script.onload = () => resolve(true);
      script.onerror = () => resolve(false);
      document.body.appendChild(script);
    });
  }, []);

  const initiatePayment = useCallback(async (options: RazorpayOptions) => {
    const loaded = await loadScript();
    if (!loaded) {
      throw new Error('Razorpay SDK failed to load');
    }

    return new Promise((resolve, reject) => {
      const razorpay = new (window as any).Razorpay({
        ...options,
        handler: (response: RazorpayResponse) => {
          resolve(response);
        },
        modal: {
          ondismiss: () => {
            reject(new Error('Payment cancelled by user'));
          },
          escape: false,
          backdropclose: false,
        },
      });

      razorpay.open();
    });
  }, []);

  return { initiatePayment };
}

// Usage in component
function PaymentButton({ bookingId, amount }: PaymentProps) {
  const { initiatePayment } = useRazorpay();
  const verifyPayment = useVerifyPayment();

  const handlePayment = async () => {
    try {
      // 1. Create order on backend
      const order = await api.payments.createOrder({
        bookingId,
        amount: amount * 100, // Convert to paise
      });

      // 2. Initialize Razorpay
      const response = await initiatePayment({
        key: order.key_id,
        amount: order.amount,
        currency: order.currency,
        name: 'Zippy Logitech',
        description: `Booking #${bookingId}`,
        order_id: order.order_id,
        prefill: {
          name: user.name,
          email: user.email,
          contact: user.phone,
        },
        notes: {
          booking_id: bookingId,
        },
        theme: {
          color: '#2563eb',
        },
      });

      // 3. Verify payment on backend
      await verifyPayment.mutateAsync({
        orderId: response.razorpay_order_id,
        paymentId: response.razorpay_payment_id,
        signature: response.razorpay_signature,
      });

      toast.success('Payment successful!');
    } catch (error) {
      toast.error('Payment failed. Please try again.');
    }
  };

  return (
    <Button onClick={handlePayment} size="lg" className="w-full">
      Pay ₹{amount}
    </Button>
  );
}
```

#### 2.1.3 React Native Integration

```typescript
// React Native Razorpay integration
import RazorpayCheckout from 'react-native-razorpay';

async function initiatePaymentRN(orderDetails: OrderDetails) {
  const options = {
    description: `Booking #${orderDetails.bookingId}`,
    image: require('./assets/logo.png'),
    currency: 'INR',
    key: RAZORPAY_KEY_ID,
    amount: orderDetails.amount * 100,
    name: 'Zippy Logitech',
    order_id: orderDetails.orderId,
    prefill: {
      email: user.email,
      contact: user.phone,
      name: user.name,
    },
    theme: { color: '#2563eb' },
  };

  try {
    const data = await RazorpayCheckout.open(options);
    
    // Verify on backend
    await api.payments.verify({
      orderId: data.razorpay_order_id,
      paymentId: data.razorpay_payment_id,
      signature: data.razorpay_signature,
    });
    
    return { success: true };
  } catch (error) {
    console.log('Payment error:', error);
    return { success: false, error };
  }
}
```

---

### 2.2 Payment Methods Support

| Method | Support Level | Notes |
|--------|---------------|-------|
| **UPI** | ✅ Full | Google Pay, PhonePe, Paytm, BHIM |
| **Cards** | ✅ Full | Visa, Mastercard, RuPay, Amex |
| **Net Banking** | ✅ Full | 50+ banks supported |
| **Wallets** | ✅ Full | Paytm, PhonePe, Amazon Pay, etc. |
| **Pay Later** | ✅ Available | ICICI, HDFC, SBI Card |
| **EMI** | ✅ Available | 3-24 months options |
| **NEFT/RTGS** | ⚠️ Manual | For corporate bookings > ₹2L |
| **Cash on Delivery** | ✅ Supported | ₹500 handling fee |

---

### 2.3 Escrow & Split Payments

```python
# Escrow for COD orders
class EscrowService:
    """
    Escrow flow:
    1. Customer pays full amount + fee
    2. Amount held in escrow
    3. Driver delivers → confirms POD
    4. Platform fee deducted
    5. Driver receives net amount
    6. Customer receives confirmation
    """
    
    async def create_escrow_payment(self, booking: Booking) -> dict:
        """Create escrow for COD orders"""
        total_amount = booking.total_amount + ESCROW_FEE  # ₹500
        
        order = await payment_service.create_order(PaymentOrderRequest(
            amount=total_amount * 100,  # paise
            currency="INR",
            receipt=f"ESC_{booking.id}",
            notes={
                "booking_id": booking.id,
                "type": "escrow",
                "driver_id": booking.driver_id,
                "platform_fee": booking.platform_fee * 100,
                "driver_earnings": (booking.total_amount - booking.platform_fee) * 100,
            }
        ))
        
        return order
    
    async def release_escrow(self, booking_id: str) -> dict:
        """Release payment to driver after delivery confirmation"""
        booking = await self._get_booking(booking_id)
        
        # Calculate split
        platform_fee = booking.platform_fee
        driver_earnings = booking.total_amount - platform_fee
        
        # Transfer to driver
        await self._transfer_to_driver(
            driver_id=booking.driver_id,
            amount=driver_earnings,
            booking_id=booking_id
        )
        
        # Mark escrow released
        await self._update_escrow_status(booking_id, "released")
        
        return {
            "driver_earnings": driver_earnings,
            "platform_fee": platform_fee,
            "released_at": datetime.utcnow(),
        }
```

---

### 2.4 Refund Policy

| Scenario | Refund Eligibility | Processing Time |
|----------|---------------------|-----------------|
| **Driver not assigned** | 100% refund | Instant |
| **Driver cancelled** | 100% refund | Instant |
| **Customer cancelled (before pickup)** | 100% - platform fee | 3-5 business days |
| **Customer cancelled (after pickup)** | 50% refund | 3-5 business days |
| **Service failure** | 100% + compensation | 7 business days |
| **Force majeure** | Case by case | 7-14 business days |

```python
# Refund policy implementation
class RefundPolicy:
    POLICIES = {
        "DRIVER_NOT_ASSIGNED": {
            "percentage": 100,
            "platform_fee_refundable": True,
            "timeline": "instant",
        },
        "BEFORE_PICKUP": {
            "percentage": 95,  # Minus 5% platform fee
            "platform_fee_refundable": False,
            "timeline": "3-5_days",
        },
        "AFTER_PICKUP": {
            "percentage": 50,
            "platform_fee_refundable": False,
            "timeline": "3-5_days",
        },
        "SERVICE_FAILURE": {
            "percentage": 100,
            "compensation": True,
            "timeline": "7_days",
        },
    }
    
    async def calculate_refund(self, booking: Booking, reason: str) -> dict:
        """Calculate refund amount based on policy"""
        policy = self.POLICIES.get(reason)
        if not policy:
            raise ValueError(f"Unknown refund reason: {reason}")
        
        refund_amount = (booking.total_amount * policy["percentage"]) / 100
        
        return {
            "refund_amount": refund_amount,
            "original_amount": booking.total_amount,
            "platform_fee_retained": 0 if policy["platform_fee_refundable"] else booking.platform_fee,
            "timeline": policy["timeline"],
            "reason": reason,
        }
```

---

## 3. GST Compliance

### 3.1 Business Registration

```yaml
# Business Structure for Zippy Logitech
entity_type: Private Limited Company
gst_registration:
  type: Regular (not Composition)
  states:
    - Tamil Nadu (Principal)
    - Karnataka
    - Andhra Pradesh
    - Kerala
    - Telangana
  hsn_codes:
    primary: 9965  # Goods transport services
    secondary: 9967  # Supporting transport services

# GST Rates
gst_rates:
  transport_services: 12%  # IGST for inter-state, SGST+CGST for intra-state
  platform_fee: 18%  # Commission/fees
  insurance: 18%
  value_added_services: 18%

# Registration Numbers (Example)
tin_numbers:
  tn: 33AABCU9603R1ZX
  ka: 29AABCU9603R1Z3
  ap: 37AABCU9603R1Z1
  kl: 32AABCU9603R1Z0
  tg: 36AABCU9603R1Z2
```

---

### 3.2 Invoice Generation

```python
# models/invoice.py
from datetime import datetime
from pydantic import BaseModel
from typing import Literal

class InvoiceLineItem(BaseModel):
    description: str
    hsn_code: str
    quantity: float
    unit: str
    rate: float
    amount: float
    gst_rate: float
    cgst: float
    sgst: float
    igst: float
    total: float

class Invoice(BaseModel):
    invoice_number: str  # ZL-2024-000001
    invoice_date: datetime
    booking_id: str
    customer: {
        "name": str,
        "gstin": str | None,
        "address": str,
        "state_code": str,  # 33 for TN
    }
    supplier: {
        "name": "Zippy Logitech Pvt Ltd",
        "gstin": str,
        "address": str,
        "state_code": str,
    }
    line_items: list[InvoiceLineItem]
    sub_total: float
    total_cgst: float
    total_sgst: float
    total_igst: float
    total_gst: float
    grand_total: float
    is_interstate: bool
    reverse_charge: bool = False
    
class InvoiceService:
    """Generate GST-compliant invoices"""
    
    HSN_CODES = {
        "road_freight": "996511",
        "logistics_service": "996531",
        "handling_charges": "996712",
        "insurance": "9971",
        "platform_fee": "9967",
    }
    
    GST_RATES = {
        "transport": 12.0,
        "services": 18.0,
        "insurance": 18.0,
    }
    
    async def generate_invoice(self, booking: Booking) -> Invoice:
        """Generate invoice for completed booking"""
        
        # Determine GST type (IGST vs CGST+SGST)
        origin_state = booking.pickup_address.state_code
        dest_state = booking.delivery_address.state_code
        is_interstate = origin_state != dest_state
        
        line_items = []
        
        # 1. Freight Charges
        freight_item = self._create_line_item(
            description=f"Road Freight: {booking.pickup_address.city} to {booking.delivery_address.city}",
            hsn_code=self.HSN_CODES["road_freight"],
            quantity=1,
            unit="JOB",
            rate=booking.base_cost + booking.scenario_surcharge,
            gst_rate=self.GST_RATES["transport"],
            is_interstate=is_interstate,
        )
        line_items.append(freight_item)
        
        # 2. Platform Fee (always 18%)
        platform_item = self._create_line_item(
            description="Platform Service Fee",
            hsn_code=self.HSN_CODES["platform_fee"],
            quantity=1,
            unit="JOB",
            rate=booking.platform_fee,
            gst_rate=self.GST_RATES["services"],
            is_interstate=is_interstate,
        )
        line_items.append(platform_item)
        
        # 3. Insurance (if opted)
        if booking.insurance_amount > 0:
            insurance_item = self._create_line_item(
                description="Transit Insurance",
                hsn_code=self.HSN_CODES["insurance"],
                quantity=1,
                unit="JOB",
                rate=booking.insurance_amount,
                gst_rate=self.GST_RATES["insurance"],
                is_interstate=is_interstate,
            )
            line_items.append(insurance_item)
        
        # Calculate totals
        sub_total = sum(item.amount for item in line_items)
        
        if is_interstate:
            total_igst = sum(item.igst for item in line_items)
            total_cgst = total_sgst = 0
        else:
            total_igst = 0
            total_cgst = sum(item.cgst for item in line_items)
            total_sgst = sum(item.sgst for item in line_items)
        
        invoice = Invoice(
            invoice_number=await self._generate_invoice_number(),
            invoice_date=datetime.utcnow(),
            booking_id=booking.id,
            customer={
                "name": booking.customer.name,
                "gstin": booking.customer.gstin,
                "address": booking.customer.address,
                "state_code": booking.customer.state_code,
            },
            supplier={
                "name": "Zippy Logitech Pvt Ltd",
                "gstin": f"33AABCU9603R1ZX",  # TN GSTIN
                "address": "Chennai, Tamil Nadu",
                "state_code": "33",
            },
            line_items=line_items,
            sub_total=sub_total,
            total_cgst=total_cgst,
            total_sgst=total_sgst,
            total_igst=total_igst,
            total_gst=total_cgst + total_sgst + total_igst,
            grand_total=sub_total + total_cgst + total_sgst + total_igst,
            is_interstate=is_interstate,
        )
        
        # Save to database
        await self._save_invoice(invoice)
        
        return invoice
    
    def _create_line_item(
        self,
        description: str,
        hsn_code: str,
        quantity: float,
        unit: str,
        rate: float,
        gst_rate: float,
        is_interstate: bool,
    ) -> InvoiceLineItem:
        """Create a single line item with GST calculations"""
        
        amount = rate * quantity
        
        if is_interstate:
            # IGST = rate * amount / 100
            igst = (gst_rate * amount) / 100
            cgst = sgst = 0
        else:
            # CGST = SGST = (rate/2) * amount / 100
            half_rate = gst_rate / 2
            cgst = (half_rate * amount) / 100
            sgst = (half_rate * amount) / 100
            igst = 0
        
        total = amount + cgst + sgst + igst
        
        return InvoiceLineItem(
            description=description,
            hsn_code=hsn_code,
            quantity=quantity,
            unit=unit,
            rate=rate,
            amount=amount,
            gst_rate=gst_rate,
            cgst=cgst,
            sgst=sgst,
            igst=igst,
            total=total,
        )
```

---

### 3.3 Invoice Template (PDF Generation)

```python
# services/invoice/pdf_generator.py
from fpdf import FPDF
from typing import List

class GSTInvoicePDF(FPDF):
    def __init__(self, invoice: Invoice):
        super().__init__()
        self.invoice = invoice
        
    def generate(self) -> bytes:
        self.add_page()
        self.set_auto_page_break(auto=True, margin=15)
        
        # Header
        self._add_header()
        
        # Party Details
        self._add_party_details()
        
        # Line Items Table
        self._add_line_items()
        
        # Totals
        self._add_totals()
        
        # Footer
        self._add_footer()
        
        return self.output(dest='S').encode('latin1')
    
    def _add_header(self):
        # Company Logo & Name
        self.set_font('Arial', 'B', 20)
        self.cell(0, 10, 'Zippy Logitech Pvt Ltd', ln=True, align='C')
        
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'GST Invoice', ln=True, align='C')
        self.ln(5)
        
        # Invoice Details
        self.set_font('Arial', '', 10)
        self.cell(95, 6, f'Invoice No: {self.invoice.invoice_number}', ln=0)
        self.cell(95, 6, f'Date: {self.invoice.invoice_date.strftime("%d-%m-%Y")}', ln=1, align='R')
        self.cell(95, 6, f'Booking ID: {self.invoice.booking_id}', ln=1)
        self.ln(5)
    
    def _add_party_details(self):
        # Billed To
        self.set_font('Arial', 'B', 10)
        self.cell(95, 6, 'Billed To:', ln=0)
        self.cell(95, 6, 'Billed By:', ln=1)
        
        self.set_font('Arial', '', 10)
        self.cell(95, 5, self.invoice.customer["name"], ln=0)
        self.cell(95, 5, self.invoice.supplier["name"], ln=1)
        
        if self.invoice.customer.get("gstin"):
            self.cell(95, 5, f'GSTIN: {self.invoice.customer["gstin"]}', ln=0)
        self.cell(95, 5, f'GSTIN: {self.invoice.supplier["gstin"]}', ln=1)
        
        self.cell(95, 5, self.invoice.customer["address"], ln=0)
        self.cell(95, 5, self.invoice.supplier["address"], ln=1)
        self.ln(5)
        
        # Place of Supply
        self.set_font('Arial', 'B', 10)
        self.cell(0, 6, f'Place of Supply: {self.invoice.customer["state_code"]}', ln=1)
        self.ln(3)
    
    def _add_line_items(self):
        # Table Header
        self.set_fill_color(240, 240, 240)
        self.set_font('Arial', 'B', 9)
        
        headers = ['Description', 'HSN', 'Qty', 'Rate', 'Amount', 'GST', 'Total']
        widths = [50, 20, 15, 25, 25, 20, 25]
        
        for header, width in zip(headers, widths):
            self.cell(width, 8, header, border=1, fill=True, align='C')
        self.ln()
        
        # Table Body
        self.set_font('Arial', '', 9)
        for item in self.invoice.line_items:
            self.cell(50, 6, item.description[:30], border=1)
            self.cell(20, 6, item.hsn_code, border=1, align='C')
            self.cell(15, 6, f'{item.quantity} {item.unit}', border=1, align='C')
            self.cell(25, 6, f'₹{item.rate:.2f}', border=1, align='R')
            self.cell(25, 6, f'₹{item.amount:.2f}', border=1, align='R')
            self.cell(20, 6, f'{item.gst_rate}%', border=1, align='C')
            self.cell(25, 6, f'₹{item.total:.2f}', border=1, align='R')
            self.ln()
    
    def _add_totals(self):
        self.ln(3)
        self.set_font('Arial', 'B', 10)
        
        # Right-aligned totals
        self.cell(130, 6, '', ln=0)
        self.cell(40, 6, 'Sub Total:', ln=0, align='R')
        self.cell(30, 6, f'₹{self.invoice.sub_total:.2f}', ln=1, align='R')
        
        if self.invoice.is_interstate:
            self.cell(130, 6, '', ln=0)
            self.cell(40, 6, f'IGST ({self.invoice.total_gst_rate}%):', ln=0, align='R')
            self.cell(30, 6, f'₹{self.invoice.total_igst:.2f}', ln=1, align='R')
        else:
            self.cell(130, 6, '', ln=0)
            self.cell(40, 6, f'CGST ({self.invoice.total_gst_rate/2}%):', ln=0, align='R')
            self.cell(30, 6, f'₹{self.invoice.total_cgst:.2f}', ln=1, align='R')
            
            self.cell(130, 6, '', ln=0)
            self.cell(40, 6, f'SGST ({self.invoice.total_gst_rate/2}%):', ln=0, align='R')
            self.cell(30, 6, f'₹{self.invoice.total_sgst:.2f}', ln=1, align='R')
        
        self.set_font('Arial', 'B', 12)
        self.cell(130, 8, '', ln=0)
        self.cell(40, 8, 'Grand Total:', ln=0, align='R')
        self.cell(30, 8, f'₹{self.invoice.grand_total:.2f}', ln=1, align='R')
    
    def _add_footer(self):
        self.ln(10)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 5, 'This is a computer generated invoice and does not require signature.', ln=1, align='C')
        
        # QR Code placeholder for e-invoicing (if applicable)
        if self.invoice.grand_total > 50000:  # E-invoicing threshold
            self.ln(5)
            self.cell(0, 5, 'IRN: abc123def456... (E-invoice registered)', ln=1, align='C')
```

---

## 4. E-Way Bill Integration

### 4.1 E-Way Bill Requirements

| Scenario | E-Way Bill Required | Threshold |
|----------|---------------------|-----------|
| **Inter-state movement** | Yes | ₹50,000+ |
| **Intra-state (most states)** | Yes | ₹50,000+ |
| **Intra-state (some states)** | Yes | ₹1,00,000+ |
| **Within same city** | No | N/A |
| **Transit through multiple states** | Yes | ₹50,000+ |

### 4.2 NIC API Integration

```python
# services/compliance/eway_bill.py
import requests
from datetime import datetime, timedelta
import json

class EWayBillService:
    """
    E-Way Bill Generation via NIC API
    """
    
    NIC_API_BASE = "https://ewaybillgst.gov.in/api/v1"
    
    def __init__(self):
        self.gstin = "33AABCU9603R1ZX"  # Your GSTIN
        self.username = "your_nic_username"
        self.password = "your_nic_password"
        
    async def generate_eway_bill(self, booking: Booking, invoice: Invoice) -> dict:
        """
        Generate e-way bill for qualifying shipments
        """
        # Check if required
        if invoice.grand_total < 50000:
            return {"required": False, "reason": "Below threshold"}
        
        # Determine validity (1 day per 100km, min 1 day, max 15 days)
        distance_km = booking.route.distance_km
        validity_days = min(max(1, distance_km // 100 + 1), 15)
        
        payload = {
            "supplyType": "O",  # Outward
            "subSupplyType": 1,  # Supply
            "docType": "INV",  # Invoice
            "docNo": invoice.invoice_number,
            "docDate": invoice.invoice_date.strftime("%d/%m/%Y"),
            "fromGstin": self.gstin,
            "fromTrdName": "Zippy Logitech Pvt Ltd",
            "fromAddr1": booking.pickup_address.address_line1,
            "fromAddr2": booking.pickup_address.address_line2 or "",
            "fromPlace": booking.pickup_address.city,
            "fromPincode": int(booking.pickup_address.pincode),
            "fromStateCode": int(booking.pickup_address.state_code),
            "toGstin": booking.customer.gstin or "URP",  # Unregistered Person
            "toTrdName": booking.customer.name,
            "toAddr1": booking.delivery_address.address_line1,
            "toAddr2": booking.delivery_address.address_line2 or "",
            "toPlace": booking.delivery_address.city,
            "toPincode": int(booking.delivery_address.pincode),
            "toStateCode": int(booking.delivery_address.state_code),
            "transMode": 1,  # Road
            "transDistance": distance_km,
            "transporterName": booking.driver.name if booking.driver else "",
            "transporterId": "",  # If registered transporter
            "transDocNo": "",
            "transDocDate": "",
            "vehicleNo": booking.vehicle.number if booking.vehicle else "",
            "vehicleType": "R",  # Regular
            "itemList": [
                {
                    "productName": booking.material.type,
                    "productDesc": booking.material.description,
                    "hsnCode": int(invoice.line_items[0].hsn_code),
                    "quantity": booking.material.weight,
                    "qtyUnit": "KGS",
                    "taxableAmount": invoice.sub_total,
                    "cgstRate": invoice.line_items[0].gst_rate / 2 if not invoice.is_interstate else 0,
                    "sgstRate": invoice.line_items[0].gst_rate / 2 if not invoice.is_interstate else 0,
                    "igstRate": invoice.line_items[0].gst_rate if invoice.is_interstate else 0,
                    "cessRate": 0,
                    "cessNonAdvol": 0,
                }
            ],
            "totInvValue": invoice.grand_total,
        }
        
        try:
            response = requests.post(
                f"{self.NIC_API_BASE}/ewaybill",
                json=payload,
                headers={
                    "Authorization": f"Bearer {await self._get_auth_token()}",
                    "Content-Type": "application/json",
                }
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Save to database
            eway_bill = EWayBill(
                booking_id=booking.id,
                ewb_number=result["ewayBillNo"],
                ewb_date=datetime.strptime(result["ewayBillDate"], "%d/%m/%Y %I:%M:%S %p"),
                valid_until=datetime.strptime(result["validUpto"], "%d/%m/%Y %I:%M:%S %p"),
                qr_code=result.get("qrCode"),
                qr_code_data=result.get("qrCodeUrl"),
            )
            await self._save_eway_bill(eway_bill)
            
            return {
                "success": True,
                "eway_bill_no": result["ewayBillNo"],
                "eway_bill_date": result["ewayBillDate"],
                "valid_until": result["validUpto"],
                "qr_code_url": result.get("qrCodeUrl"),
            }
            
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=400, detail=f"E-way bill generation failed: {str(e)}")
    
    async def update_vehicle_number(self, ewb_number: str, vehicle_no: str) -> dict:
        """
        Update vehicle number (for vehicle changes)
        """
        payload = {
            "ewbNo": ewb_number,
            "vehicleNo": vehicle_no,
            "fromPlace": "",
            "fromState": 0,
            "reasonCode": 2,  # Vehicle breakdown
            "reasonRem": "Vehicle changed due to breakdown",
            "transDocNo": "",
            "transDocDate": "",
            "transMode": 1,
        }
        
        response = requests.post(
            f"{self.NIC_API_BASE}/ewaybill/updatevehicle",
            json=payload,
            headers={"Authorization": f"Bearer {await self._get_auth_token()}"},
        )
        
        return response.json()
    
    async def extend_validity(self, ewb_number: str, extension_days: int) -> dict:
        """
        Extend e-way bill validity (if needed)
        """
        payload = {
            "ewbNo": ewb_number,
            "vehicleNo": "",
            "fromPlace": "",
            "fromState": 0,
            "remainingDistance": 0,
            "extnRsnCode": 1,  # Natural calamity, law and order, etc.
            "extnRsnRem": "Delay due to traffic conditions",
        }
        
        response = requests.post(
            f"{self.NIC_API_BASE}/ewaybill/extendvalidity",
            json=payload,
            headers={"Authorization": f"Bearer {await self._get_auth_token()}"},
        )
        
        return response.json()
```

---

### 4.3 E-Way Bill in Driver App

```typescript
// Driver app e-way bill display
interface EWayBillData {
  ewbNumber: string;
  ewbDate: string;
  validUntil: string;
  qrCodeUrl: string;
  from: {
    name: string;
    address: string;
    gstin: string;
  };
  to: {
    name: string;
    address: string;
    gstin: string;
  };
  vehicleNumber: string;
  items: Array<{
    name: string;
    hsnCode: string;
    quantity: number;
    value: number;
  }>;
}

// Component for displaying e-way bill
function EWayBillCard({ data }: { data: EWayBillData }) {
  const isValid = new Date(data.validUntil) > new Date();
  
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>🚛 E-Way Bill</Text>
        <Badge variant={isValid ? 'success' : 'danger'}>
          {isValid ? 'VALID' : 'EXPIRED'}
        </Badge>
      </View>
      
      <View style={styles.details}>
        <Text style={styles.label}>E-Way Bill No:</Text>
        <Text style={styles.value}>{data.ewbNumber}</Text>
        
        <Text style={styles.label}>Valid Until:</Text>
        <Text style={styles.value}>{formatDate(data.validUntil)}</Text>
        
        <Text style={styles.label}>Vehicle:</Text>
        <Text style={styles.value}>{data.vehicleNumber}</Text>
      </View>
      
      <View style={styles.qrContainer}>
        <Image 
          source={{ uri: data.qrCodeUrl }} 
          style={styles.qrCode}
          resizeMode="contain"
        />
        <Text style={styles.qrLabel}>Show for verification</Text>
      </View>
      
      <Button 
        variant="secondary" 
        onPress={() => downloadEWayBill(data.ewbNumber)}
      >
        📥 Download PDF
      </Button>
    </View>
  );
}
```

---

## 5. Insurance Integration

### 5.1 Transit Insurance

```python
# services/insurance/transit_insurance.py
class TransitInsuranceService:
    """
    Goods transit insurance via ICICI Lombard / Bajaj Alliance
    """
    
    PREMIUM_RATE = 0.01  # 1% of declared value
    MIN_PREMIUM = 500  # ₹500 minimum
    MAX_COVERAGE = 5000000  # ₹50 lakhs max
    
    async def calculate_premium(self, declared_value: int) -> dict:
        """Calculate insurance premium"""
        if declared_value <= 0:
            return {"required": False, "premium": 0}
        
        premium = max(declared_value * self.PREMIUM_RATE, self.MIN_PREMIUM)
        coverage = min(declared_value, self.MAX_COVERAGE)
        
        return {
            "required": True,
            "declared_value": declared_value,
            "premium": round(premium, 2),
            "coverage_amount": coverage,
            "gst": round(premium * 0.18, 2),
            "total": round(premium * 1.18, 2),
        }
    
    async def purchase_policy(
        self,
        booking: Booking,
        declared_value: int,
        customer_details: dict,
    ) -> dict:
        """Purchase transit insurance policy"""
        
        premium = await self.calculate_premium(declared_value)
        
        policy_payload = {
            "policy_type": "SINGLE_TRANSIT",
            "transit_mode": "ROAD",
            "packing": "CONTAINERIZED",  # or OPEN
            "from_location": {
                "city": booking.pickup_address.city,
                "state": booking.pickup_address.state,
                "pincode": booking.pickup_address.pincode,
            },
            "to_location": {
                "city": booking.delivery_address.city,
                "state": booking.delivery_address.state,
                "pincode": booking.delivery_address.pincode,
            },
            "consignor": {
                "name": customer_details["name"],
                "address": booking.pickup_address.full_address,
                "gstin": customer_details.get("gstin"),
            },
            "consignee": {
                "name": booking.delivery_contact.name,
                "address": booking.delivery_address.full_address,
            },
            "commodity": {
                "description": booking.material.type,
                "hsn_code": "9965",
                "value": declared_value,
                "weight": booking.material.weight,
            },
            "vehicle_details": {
                "number": booking.vehicle.number,
                "type": booking.vehicle.type,
            },
            "premium": premium["premium"],
            "sum_insured": declared_value,
            "policy_start_date": datetime.utcnow().isoformat(),
            "policy_end_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
        }
        
        # Call insurance provider API
        try:
            response = await self._call_insurance_api("/transit/policy", policy_payload)
            
            policy = InsurancePolicy(
                booking_id=booking.id,
                policy_number=response["policy_number"],
                provider=response["provider"],
                sum_insured=declared_value,
                premium=premium["total"],
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=7),
                certificate_url=response["certificate_url"],
            )
            
            await self._save_policy(policy)
            
            return {
                "success": True,
                "policy_number": response["policy_number"],
                "certificate_url": response["certificate_url"],
                "premium": premium["total"],
                "coverage": declared_value,
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Insurance purchase failed: {str(e)}")
    
    async def file_claim(
        self,
        policy_number: str,
        claim_details: dict,
        documents: list[UploadFile],
    ) -> dict:
        """File insurance claim for damaged/lost goods"""
        
        claim_payload = {
            "policy_number": policy_number,
            "claim_type": claim_details["type"],  # DAMAGE, LOSS, THEFT
            "incident_date": claim_details["date"],
            "incident_location": claim_details["location"],
            "description": claim_details["description"],
            "estimated_loss": claim_details["estimated_loss"],
            "documents": await self._upload_documents(documents),
        }
        
        response = await self._call_insurance_api("/claims", claim_payload)
        
        return {
            "claim_number": response["claim_number"],
            "status": "SUBMITTED",
            "expected_resolution": "7-14 business days",
        }
```

---

## 6. KYC & Document Verification

### 6.1 Driver KYC

```python
# services/kyc/driver_kyc.py
class DriverKYCService:
    """
    Driver document verification via Digio / Karza
    """
    
    REQUIRED_DOCUMENTS = {
        "DRIVING_LICENSE": {
            "required": True,
            "verification": "OCR + Government DB",
            "validity_check": True,
        },
        "VEHICLE_REGISTRATION": {
            "required": True,
            "verification": "OCR + Vahan DB",
            "validity_check": True,
        },
        "INSURANCE": {
            "required": True,
            "verification": "OCR + Manual",
            "validity_check": True,
        },
        "FITNESS_CERTIFICATE": {
            "required": True,  # For commercial vehicles
            "verification": "Vahan DB",
            "validity_check": True,
        },
        "PERMIT": {
            "required": True,  # For interstate
            "verification": "OCR",
            "validity_check": True,
        },
        "PAN_CARD": {
            "required": True,
            "verification": "NSDL API",
            "validity_check": True,
        },
        "BANK_ACCOUNT": {
            "required": True,
            "verification": "Penny Drop",
            "validity_check": True,
        },
    }
    
    async def verify_document(
        self,
        driver_id: str,
        document_type: str,
        document_file: UploadFile,
    ) -> dict:
        """Verify uploaded document"""
        
        # 1. OCR Extraction
        ocr_result = await self._extract_text(document_file)
        
        # 2. Database verification
        if document_type == "DRIVING_LICENSE":
            verification = await self._verify_driving_license(
                license_number=ocr_result["license_number"],
                dob=ocr_result["dob"],
            )
        elif document_type == "VEHICLE_REGISTRATION":
            verification = await self._verify_vehicle_registration(
                reg_number=ocr_result["registration_number"],
            )
        elif document_type == "PAN_CARD":
            verification = await self._verify_pan(
                pan_number=ocr_result["pan_number"],
                name=ocr_result["name"],
            )
        
        # 3. Save verification result
        doc_record = DriverDocument(
            driver_id=driver_id,
            document_type=document_type,
            document_number=ocr_result.get("document_number"),
            verification_status=verification["status"],
            verified_at=datetime.utcnow() if verification["status"] == "VERIFIED" else None,
            expiry_date=verification.get("expiry_date"),
            document_url=await self._save_document(document_file),
            extracted_data=ocr_result,
        )
        
        await self._save_document_record(doc_record)
        
        return {
            "document_type": document_type,
            "status": verification["status"],
            "document_number": ocr_result.get("document_number"),
            "expiry_date": verification.get("expiry_date"),
            "validity_days": verification.get("validity_days"),
        }
    
    async def _verify_driving_license(self, license_number: str, dob: str) -> dict:
        """Verify driving license via Karza API"""
        
        response = await http_client.post(
            "https://api.karza.in/v3/dl-verification",
            json={
                "consent": "Y",
                "dlNo": license_number,
                "dob": dob,
            },
            headers={"x-karza-key": KARZA_API_KEY},
        )
        
        data = response.json()
        
        return {
            "status": "VERIFIED" if data["status"] == "SUCCESS" else "FAILED",
            "license_number": data["result"]["dlNumber"],
            "holder_name": data["result"]["name"],
            "valid_from": data["result"]["validFrom"],
            "valid_until": data["result"]["validTo"],
            "vehicle_classes": data["result"]["vehicleClass"],
            "validity_days": (datetime.strptime(data["result"]["validTo"], "%Y-%m-%d") - datetime.utcnow()).days,
        }
    
    async def _verify_vehicle_registration(self, reg_number: str) -> dict:
        """Verify vehicle via Vahan API"""
        
        response = await http_client.post(
            "https://vahan.parivahan.gov.in/api/vehicle-details",
            json={"registration_number": reg_number},
        )
        
        data = response.json()
        
        return {
            "status": "VERIFIED",
            "registration_number": data["regNumber"],
            "owner_name": data["ownerName"],
            "vehicle_class": data["vehicleClass"],
            "fuel_type": data["fuelType"],
            "registration_date": data["registrationDate"],
            "fitness_upto": data["fitnessUpto"],
            "insurance_upto": data["insuranceUpto"],
            "tax_upto": data["taxUpto"],
        }
```

---

## 7. Compliance Checklist

### 7.1 Pre-Booking Compliance

- [ ] Customer GSTIN validation (if provided)
- [ ] Driver document verification (DL, RC, Insurance)
- [ ] Vehicle fitness certificate validity
- [ ] Route permits for interstate movement

### 7.2 During Transit Compliance

- [ ] E-way bill generated (if > ₹50,000)
- [ ] Driver app tracking active
- [ ] Vehicle GPS operational
- [ ] LHC (Lorry Hire Challan) generated

### 7.3 Post-Delivery Compliance

- [ ] GST invoice generated and emailed
- [ ] E-way bill part B updated (if vehicle changed)
- [ ] POD uploaded and verified
- [ ] Payment reconciliation complete

---

## 8. Implementation Roadmap

| Phase | Duration | Tasks |
|-------|----------|-------|
| **Week 1** | 5 days | Razorpay integration (backend + frontend) |
| **Week 2** | 5 days | GST invoice generation, PDF templates |
| **Week 3** | 5 days | E-way bill NIC API integration |
| **Week 4** | 5 days | Insurance integration, KYC document verification |
| **Week 5** | 5 days | Testing, compliance audits, documentation |

---

## 9. Integration Summary

| Service | Provider | API Type | Status |
|---------|----------|----------|--------|
| **Payments** | Razorpay | REST + Webhooks | ✅ Core |
| **GST Invoicing** | In-house + GSP | REST | ✅ Core |
| **E-Way Bill** | NIC India | REST | ✅ Core |
| **Driver KYC** | Karza / Digio | REST | ✅ P1 |
| **Vehicle Verification** | Vahan | REST | ✅ P1 |
| **Insurance** | ICICI / Bajaj | REST | ✅ P1 |
| **PAN Verification** | NSDL | REST | ✅ P1 |

---

*Document Version: 1.0*
*Last Updated: April 2026*
*Total Specifications: ~500 lines*
