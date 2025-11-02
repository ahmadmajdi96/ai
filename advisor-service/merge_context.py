def build_context_bundle(analytics, rules, optimizer, ragctx):
    return {
        "analytics": analytics,
        "rules": rules,
        "optimizer": optimizer,
        "rag": ragctx
    }
