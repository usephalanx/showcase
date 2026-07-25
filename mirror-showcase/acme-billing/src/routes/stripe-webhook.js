const express = require('express');
const Stripe = require('stripe');

const db = require('../services/db');
const { grantSeats, revokeSeats } = require('../services/entitlements');

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
const router = express.Router();

router.post('/', async (req, res) => {
  let event;
  try {
    event = stripe.webhooks.constructEvent(
      req.body,
      req.headers['stripe-signature'],
      process.env.STRIPE_WEBHOOK_SECRET,
    );
  } catch (err) {
    return res.status(400).send(`signature check failed: ${err.message}`);
  }

  const already = await db.query(
    'select 1 from processed_events where provider = $1 and event_id = $2',
    ['stripe', event.id],
  );
  if (already.rowCount > 0) return res.json({ received: true });

  const obj = event.data.object;

  switch (event.type) {
    case 'checkout.session.completed':
      await grantSeats(obj.client_reference_id, obj.metadata.seats, {
        provider: 'stripe',
        reference: obj.id,
      });
      break;
    case 'customer.subscription.deleted':
      await revokeSeats(obj.metadata.workspace_id, { provider: 'stripe' });
      break;
    default:
      break;
  }

  await db.query(
    'insert into processed_events (provider, event_id, seen_at) values ($1, $2, now())',
    ['stripe', event.id],
  );

  res.json({ received: true });
});

module.exports = router;
