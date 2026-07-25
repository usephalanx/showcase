const { clerkMiddleware, requireAuth } = require('@clerk/express');

// Gate the dashboard + checkout behind a Clerk session.
function withAuth(app) {
  app.use(clerkMiddleware());
}

function protect(req, res, next) {
  return requireAuth()(req, res, next);
}

module.exports = { withAuth, protect };
