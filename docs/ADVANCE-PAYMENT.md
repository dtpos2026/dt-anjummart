# Advance Cash Payment (Save Rs. 499): how it works and what to set up

Shoppers choose **Cash on Delivery** or **Advance Cash Payment** in the cart (cart page and cart drawer). Advance Cash
Payment shows the bold "SAVE RS. 499" banner, the original total, the Rs. 499 discount and the amount to pay, the
JazzCash / Easypaisa / Meezan details with Copy buttons, and the five steps. The shopper types the transaction ID,
continues to checkout (the discount code is applied for them) and places the order. **The theme never marks anything as
paid.** The order stays "Payment pending" until you verify the money and mark it paid.

## What runs where

| Part | Where | Notes |
| --- | --- | --- |
| Payment choice, maths, details, Copy buttons, transaction ID | Theme (`snippets/advance-pay.liquid`, `sections/advance-pay-details.liquid`, `assets/theme.js` AdvPay, `assets/base.css`) | Switch on in Theme settings, **Advance Cash Payment**. Off by default. |
| Rs. 499 discount | Shopify discount code **ADVANCE499** (created, active, Rs. 499 off the order, one use per customer, no combining) | Applied through `/checkout?discount=ADVANCE499` when the shopper continues with Advance Cash Payment. |
| Manual payment method shown at checkout | Shopify Admin (you create it, section 1) | Cannot be created from the theme or the API. |
| Saved with the order | Cart attributes, shown on the order under "Additional details": **Payment preference**, **Transaction ID**, **Advance amount due** | Plus Shopify's own discount line, payment method and totals. |

There is no database and nothing to migrate: this is a Shopify store, so the data lives in Shopify (cart attributes, order,
discount code, theme settings).

## 1. One-time setup in Shopify (before you switch the feature on)

1. **Settings, Payments, Manual payment methods, Add manual payment method, Create custom payment method.**
   * Name: `Advance Cash Payment` (must match Theme settings, "Shopify payment method name").
   * Additional details (shown to the shopper at checkout when this method is selected): paste the text in section 5.
   * Payment instructions (sent after the order, in the e-mail and on the thank-you page): paste the text in section 5.
   * Keep **Cash on Delivery (COD)** as it is.
2. **Check the discount code**: Discounts, `ADVANCE499`. It should show "Rs499.00 off entire order, one use per customer".
3. **Theme settings, Advance Cash Payment:** tick **Offer Advance Cash Payment in the cart**. The payment details (account
   titles, numbers, IBAN) are already filled in from what you gave us; re-check every digit.
4. Publish the theme, then place **one test order each way** (Cash on Delivery and Advance Cash Payment) and cancel them.
5. Ask for the policy wording in section 6 to be put on the live pages (or paste it yourself).

## 2. What a shopper sees

1. Cart: the gold-on-black banner "SAVE RS. 499 ON ADVANCE CASH PAYMENT!" and two options. Cash on Delivery is selected by default.
2. Choosing **Advance Cash Payment** shows: original total, discount (−Rs. 499), amount to pay now, "your order will be
   confirmed after we verify your payment", the account details with Copy buttons (loaded only at that moment, they are
   not in the cart for Cash on Delivery shoppers), the five steps, the transaction ID field and a WhatsApp link for the
   payment screenshot.
3. **Checkout** is blocked until a transaction ID (6 or more characters) is typed. Then the shopper goes to Shopify checkout with
   the discount already in the order summary and chooses **Advance Cash Payment** as the payment method.
4. Switching options never stacks the discount: the cart only shows the maths; Shopify applies the code once.

## 3. How you verify and manage advance orders

Find them: **Orders**, search `discount_code:ADVANCE499`, or filter by payment method "Advance Cash Payment". Open the order:
**Additional details** shows Payment preference, **Transaction ID** and **Advance amount due**.

| Status you want | How it appears in Shopify |
| --- | --- |
| **Pending Payment** | Order status "Payment pending" (every manual payment order starts here). |
| **Payment Verification** | Shopify has no separate state. Add the tag `payment-verification` while you check it. |
| **Paid** | After you confirm the money arrived: tag `advance-verified`, then **Mark as paid**. Fulfil only after this. |
| **Cancelled** | Cancel the order (restock). Tag `advance-not-received` first if the payment never arrived. |

Verification steps: (1) open the JazzCash / Easypaisa / Meezan app or statement, (2) find a credit for the **Advance amount
due** that matches the Transaction ID (and the screenshot the customer sent on WhatsApp), (3) only then mark as paid.
**A transaction ID or a screenshot typed or sent by a customer is never proof by itself.**

### Mismatches to watch for

* **Cash on Delivery order with the ADVANCE499 discount:** the shopper used the code but chose COD. Edit the order to
  remove the discount, or ask them to pay in advance, before dispatch.
* **Advance Cash Payment order without the discount code:** they reached checkout another way. Either accept the full
  amount or apply the Rs. 499 discount by editing the order and refunding the difference.
* A shopper who first chose Advance, then switched to COD in the cart, may still see the code in checkout because Shopify
  remembers a code on an open checkout. They can remove it; if they do not, handle it as above.

### Optional automation (Shopify Flow)

In Shopify Flow you can add the tags automatically: trigger **Order created**, condition "discount code is ADVANCE499 or
payment gateway is Advance Cash Payment", action **Add order tags** `advance-payment, payment-verification`. Check the
exact field names in your Flow editor; this was not tested from here.

## 4. Limits of the Shopify Basic plan (why it is built this way)

* Checkout cannot be edited with code on this plan, so the discount banner, the Copy buttons and the transaction ID field
  live in the **cart**, and the bank details are also in the payment method's text at checkout (plain text, no buttons).
* A discount that depends on the payment method chosen inside checkout is not possible without an app or Shopify Plus.
  That is why the discount is a code applied when the shopper continues from the cart with Advance Cash Payment.
* File upload of a payment screenshot is not possible in the cart; the shopper sends it on WhatsApp.
* Checkout always lists every manual payment method; a shopper could still pick the wrong one. The order's additional
  details and the discount code make that visible (section 3).

## 5. Text to paste into the Shopify payment method

**Additional details**

```
SAVE RS. 499 ON ADVANCE CASH PAYMENT
Choose Advance Cash Payment in your cart first: the Rs. 499 discount (ADVANCE499) then appears in your order summary.
Pay the discounted amount by JazzCash, Easypaisa or Meezan Bank transfer.

JazzCash / Easypaisa
Account title: FAHEEM ABBAS ANJUM
Mobile number: 0300-7341433

Meezan Bank
Account title: FAHEEM ABBAS ANJUM
Branch: Rasheedabad Chowk, Multan
Account number: 05100107790897
IBAN: PK77MEZN0005100107790897

Your order will be confirmed after we verify your payment. Send the transaction ID and a screenshot of the payment to us on WhatsApp +92 371 4661514.
```

**Payment instructions**

```
Thank you for your order. It is waiting for payment verification and will not be dispatched until we confirm your payment.

1. Transfer the amount shown on your order to one of these accounts:
   JazzCash / Easypaisa: FAHEEM ABBAS ANJUM, 0300-7341433
   Meezan Bank: FAHEEM ABBAS ANJUM, Rasheedabad Chowk, Multan, account 05100107790897, IBAN PK77MEZN0005100107790897
2. Send your order number, the transaction ID and a screenshot of the payment on WhatsApp +92 371 4661514.
3. We verify the payment and confirm your order.
```

## 6. Policy wording (put on the live pages when you switch the feature on)

* Shipping policy, new section **Advance Cash Payment**: see `docs/policies/shipping-policy.html`.
* Refund policy, new section **Advance payments**: see `docs/policies/refund-policy.html`.

These wording choices (confirm only after verification; refund of a cancelled advance order by bank transfer or wallet in
7 to 10 working days, as for other refunds) are yours to approve.

## 7. Security notes

* The account details are public by nature (customers must see them) and live in Theme settings, not in code secrets. No
  passwords, API keys or admin credentials are stored anywhere in the theme.
* They are fetched from the theme only after a shopper chooses Advance Cash Payment, and are not in the markup of the
  Cash on Delivery view. They are, however, visible to anyone who chooses that option or opens the section URL, as intended.
* Keep the GitHub repository private: it contains the settings file with the account details.

## 8. Tests

Local suite section 2e (about 50 checks): amounts, one-time discount while switching, refresh, quantity change, validation,
checkout redirect, Cash on Delivery path unchanged, Copy buttons, drawer, phone layout, accessibility. Not tested from
here (needs your store): the real Shopify checkout screens, the real payment method list, e-mails.
