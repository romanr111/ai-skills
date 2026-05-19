# Good and Bad Tests

Load this when writing or reviewing tests for behavior quality.

## Good Tests

Good tests verify observable behavior through public interfaces and survive internal refactors.

```typescript
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);

  const result = await checkout(cart, paymentMethod);

  expect(result.status).toBe("confirmed");
});
```

Characteristics:
- tests behavior users or callers care about
- uses the public API only
- describes what the system does, not how it does it
- fails when behavior regresses, not when internals move

## Bad Tests

Implementation-detail tests couple the test suite to internal structure.

```typescript
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);

  await checkout(cart, payment);

  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

Red flags:
- mocking internal collaborators
- testing private methods
- asserting internal call counts or order
- test name describes implementation instead of behavior
- test fails after a refactor with unchanged behavior

## Verify Through the Interface

Prefer proving behavior through the same interface a caller uses.

```typescript
// Bad: bypasses the interface to inspect storage.
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });

  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);

  expect(row).toBeDefined();
});

// Good: verifies the behavior through the public API.
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });

  const retrieved = await getUser(user.id);

  expect(retrieved.name).toBe("Alice");
});
```

