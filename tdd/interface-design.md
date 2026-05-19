# Interface Design for Testability

Load this when tests require excessive setup, too many mocks, private access, or awkward assertions.

## Accept Dependencies, Do Not Create Them Internally

```typescript
// Testable
function processOrder(order, paymentGateway) {
  return paymentGateway.charge(order.total);
}

// Hard to test
function processOrder(order) {
  const gateway = new StripeGateway();
  return gateway.charge(order.total);
}
```

Passing dependencies in makes external boundaries explicit and lets tests substitute only the boundary that genuinely needs substitution.

## Return Results Where Possible

```typescript
// Testable
function calculateDiscount(cart): Discount {
  return { amount: cart.total * 0.1 };
}

// Harder to test
function applyDiscount(cart): void {
  cart.total = cart.total * 0.9;
}
```

Returning values keeps assertions close to the behavior. Mutating hidden state often forces tests to inspect internals.

## Keep Public Surfaces Small

Prefer fewer methods, fewer parameters, and domain-shaped inputs. A small public interface needs fewer tests and gives the implementation room to change.

Ask:
- can the caller express the behavior with fewer methods?
- can parameters be grouped around domain concepts?
- can complexity move behind the public boundary?

