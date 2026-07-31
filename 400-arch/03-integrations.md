# 03 — Integration Contract Skeleton: POS Client → Apollo Gateway
**Kata:** K 4.W.4 | **Consumes:** 02-containers.mmd, 03-flow-instore-cart.mmd

---

## Operation: resolveCustomerCart

Triggered when a store associate scans a customer QR code at POS. Returns the unified cart, customer identity, and per-SKU availability confidence for display in-store.

### Request

```
POST https://gateway.meridian.internal/graphql
Authorization: Bearer <POS_SERVICE_TOKEN>
Content-Type: application/json
```

```graphql
query ResolveCustomerCart($barcode: String!, $storeId: ID!) {
  resolveCustomerCart(barcode: $barcode, storeId: $storeId) {
    customerId
    loyaltyId
    cart {
      cartId
      items {
        sku
        name
        quantity
        availability {
          status        # LIKELY_AVAILABLE | LIMITED | UNKNOWN | UNAVAILABLE
          confidenceScore  # 0.0 - 1.0; omit display if null (degraded mode)
          sapSyncAgeMin    # minutes since last SAP hydration; null = unknown
        }
      }
    }
    degraded          # true = availability data unavailable; show fallback banner
  }
}
```

**Variables:**

| Field | Type | Required | Notes |
|---|---|---|---|
| `barcode` | `String` | Yes | Scanned loyalty barcode or QR payload |
| `storeId` | `ID` | Yes | Meridian store identifier; used for per-store inventory scoping |

---

### Response — success (HTTP 200)

```json
{
  "data": {
    "resolveCustomerCart": {
      "customerId": "cust_7f3a2b",
      "loyaltyId": "loyalty_eu_00492",
      "cart": {
        "cartId": "cart_ab12cd",
        "items": [
          {
            "sku": "SKU-00192-BLK-M",
            "name": "Classic Wool Coat — Black / M",
            "quantity": 1,
            "availability": {
              "status": "LIKELY_AVAILABLE",
              "confidenceScore": 0.82,
              "sapSyncAgeMin": 14
            }
          }
        ]
      },
      "degraded": false
    }
  }
}
```

---

### Response — degraded mode (HTTP 200, `degraded: true`)

Returned when inventory cache is stale AND SAP ECC is unreachable. Cart items are returned; availability fields are null.

```json
{
  "data": {
    "resolveCustomerCart": {
      "customerId": "cust_7f3a2b",
      "loyaltyId": "loyalty_eu_00492",
      "cart": {
        "cartId": "cart_ab12cd",
        "items": [
          {
            "sku": "SKU-00192-BLK-M",
            "name": "Classic Wool Coat — Black / M",
            "quantity": 1,
            "availability": {
              "status": "UNKNOWN",
              "confidenceScore": null,
              "sapSyncAgeMin": null
            }
          }
        ]
      },
      "degraded": true
    }
  }
}
```

**POS behaviour on `degraded: true`:** display cart items normally; show banner: "Stock availability unavailable — confirm with stock room before completing sale."

---

### Response — error (HTTP 200, `errors` array)

Apollo returns errors in-band with HTTP 200.

| `extensions.code` | Meaning | POS action |
|---|---|---|
| `BARCODE_NOT_FOUND` | Barcode does not resolve to a known customer | Prompt associate to search by name/email |
| `CART_NOT_FOUND` | Customer has no active cart | Display empty cart; allow manual SKU entry |
| `UNAUTHENTICATED` | POS service token expired or invalid | Trigger silent token refresh; retry once |
| `INTERNAL_SERVER_ERROR` | Unexpected gateway failure | Show "System error — retry or use manual lookup" |

---

## SLA targets

| Metric | Target | Notes |
|---|---|---|
| p95 latency (cache hit) | < 200ms | LAN POS to gateway to Redis and back |
| p95 latency (SAP fallback) | < 1000ms | Only on cache miss; SAP inline is slow path |
| Availability (gateway) | 99.9% | Degraded mode must respond — never hard fail |
| Degraded-mode response | Always returns HTTP 200 | Gateway must not 5xx when SAP is down |

---

## Security notes

- POS service token is a machine-to-machine OAuth 2.0 client credentials grant from Auth0; short-lived (1-hour TTL); auto-refreshed by POS client.
- `storeId` is authorised server-side — a POS token is scoped to its registered store; cross-store cart reads return `UNAUTHENTICATED`.
- No customer PII is logged at the gateway layer; only `customerId` (internal opaque ID) is emitted in structured logs.

---

## Open questions (to resolve before build)

| ID | Question | Owner |
|---|---|---|
| OQ-1 | Does the POS client refresh Auth0 tokens silently, or does a clerk re-login interrupt the flow? | Auth0 / David Park |
| OQ-2 | Is `storeId` sent in the QR barcode payload, or does POS inject it from device config? | POS engineering team |
| OQ-3 | What is the agreed degraded-mode banner copy? | Sarah Chen (Head of CX) |
