"""Tests for the Category CRUD endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient


class TestCreateCategory:
    """Tests for POST /api/categories."""

    def test_create_root_category(self, client: TestClient) -> None:
        """Creating a root category should return 201 with correct data."""
        response = client.post(
            "/api/categories",
            json={"name": "Engineering"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Engineering"
        assert data["slug"] == "engineering"
        assert data["parent_id"] is None
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_child_category(self, client: TestClient) -> None:
        """Creating a child category with valid parent_id should succeed."""
        parent_resp = client.post(
            "/api/categories",
            json={"name": "Development"},
        )
        parent_id = parent_resp.json()["id"]

        response = client.post(
            "/api/categories",
            json={"name": "Frontend", "parent_id": parent_id},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Frontend"
        assert data["parent_id"] == parent_id

    def test_create_category_nonexistent_parent(self, client: TestClient) -> None:
        """Creating a category with a nonexistent parent should return 404."""
        response = client.post(
            "/api/categories",
            json={"name": "Orphan", "parent_id": 9999},
        )
        assert response.status_code == 404

    def test_create_category_empty_name(self, client: TestClient) -> None:
        """Creating a category with an empty name should return 422."""
        response = client.post(
            "/api/categories",
            json={"name": ""},
        )
        assert response.status_code == 422

    def test_create_category_generates_unique_slug(self, client: TestClient) -> None:
        """Two categories with the same name should get unique slugs."""
        resp1 = client.post("/api/categories", json={"name": "Design"})
        resp2 = client.post("/api/categories", json={"name": "Design"})
        assert resp1.status_code == 201
        assert resp2.status_code == 201
        assert resp1.json()["slug"] != resp2.json()["slug"]

    def test_create_category_with_meta_fields(self, client: TestClient) -> None:
        """Creating a category with SEO meta fields should persist them."""
        response = client.post(
            "/api/categories",
            json={
                "name": "SEO Category",
                "description": "A test description",
                "meta_title": "Custom Title",
                "meta_description": "Custom Description",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["meta_title"] == "Custom Title"
        assert data["meta_description"] == "Custom Description"
        assert data["description"] == "A test description"


class TestListCategories:
    """Tests for GET /api/categories."""

    def test_list_empty(self, client: TestClient) -> None:
        """Listing categories when none exist should return an empty list."""
        response = client.get("/api/categories")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_returns_tree(self, client: TestClient) -> None:
        """Listing categories should return a nested tree structure."""
        parent_resp = client.post("/api/categories", json={"name": "Backend"})
        parent_id = parent_resp.json()["id"]
        client.post(
            "/api/categories",
            json={"name": "Python", "parent_id": parent_id},
        )
        client.post(
            "/api/categories",
            json={"name": "Go", "parent_id": parent_id},
        )

        response = client.get("/api/categories")
        assert response.status_code == 200
        tree = response.json()
        # Should have 1 root node
        assert len(tree) == 1
        assert tree[0]["name"] == "Backend"
        assert len(tree[0]["children"]) == 2
        child_names = {c["name"] for c in tree[0]["children"]}
        assert child_names == {"Python", "Go"}

    def test_list_multiple_roots(self, client: TestClient) -> None:
        """Multiple root categories should all appear at the top level."""
        client.post("/api/categories", json={"name": "Alpha"})
        client.post("/api/categories", json={"name": "Beta"})

        response = client.get("/api/categories")
        assert response.status_code == 200
        tree = response.json()
        assert len(tree) == 2


class TestGetCategory:
    """Tests for GET /api/categories/:slug."""

    def test_get_existing(self, client: TestClient) -> None:
        """Getting an existing category by slug should return it."""
        create_resp = client.post("/api/categories", json={"name": "Testing"})
        slug = create_resp.json()["slug"]

        response = client.get(f"/api/categories/{slug}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Testing"
        assert data["slug"] == slug

    def test_get_nonexistent(self, client: TestClient) -> None:
        """Getting a nonexistent category should return 404."""
        response = client.get("/api/categories/does-not-exist")
        assert response.status_code == 404

    def test_get_includes_children(self, client: TestClient) -> None:
        """Getting a category should include its direct children."""
        parent_resp = client.post("/api/categories", json={"name": "Tools"})
        parent_id = parent_resp.json()["id"]
        parent_slug = parent_resp.json()["slug"]
        client.post(
            "/api/categories",
            json={"name": "IDE", "parent_id": parent_id},
        )

        response = client.get(f"/api/categories/{parent_slug}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["children"]) == 1
        assert data["children"][0]["name"] == "IDE"


class TestUpdateCategory:
    """Tests for PUT /api/categories/:id."""

    def test_update_name(self, client: TestClient) -> None:
        """Updating the name should regenerate the slug."""
        create_resp = client.post("/api/categories", json={"name": "Old Name"})
        cat_id = create_resp.json()["id"]

        response = client.put(
            f"/api/categories/{cat_id}",
            json={"name": "New Name"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name"
        assert data["slug"] == "new-name"

    def test_update_description(self, client: TestClient) -> None:
        """Updating only description should not change slug."""
        create_resp = client.post("/api/categories", json={"name": "Stable"})
        cat_id = create_resp.json()["id"]
        original_slug = create_resp.json()["slug"]

        response = client.put(
            f"/api/categories/{cat_id}",
            json={"description": "Updated description"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["slug"] == original_slug
        assert data["description"] == "Updated description"

    def test_update_nonexistent(self, client: TestClient) -> None:
        """Updating a nonexistent category should return 404."""
        response = client.put(
            "/api/categories/9999",
            json={"name": "Ghost"},
        )
        assert response.status_code == 404

    def test_update_self_parent(self, client: TestClient) -> None:
        """Setting a category as its own parent should return 400."""
        create_resp = client.post("/api/categories", json={"name": "Loop"})
        cat_id = create_resp.json()["id"]

        response = client.put(
            f"/api/categories/{cat_id}",
            json={"parent_id": cat_id},
        )
        assert response.status_code == 400

    def test_update_circular_reference(self, client: TestClient) -> None:
        """Setting a child as the parent of its ancestor should return 400."""
        resp_a = client.post("/api/categories", json={"name": "A"})
        id_a = resp_a.json()["id"]

        resp_b = client.post(
            "/api/categories",
            json={"name": "B", "parent_id": id_a},
        )
        id_b = resp_b.json()["id"]

        # Try to make A a child of B (circular)
        response = client.put(
            f"/api/categories/{id_a}",
            json={"parent_id": id_b},
        )
        assert response.status_code == 400

    def test_update_nonexistent_parent(self, client: TestClient) -> None:
        """Setting parent_id to a nonexistent category should return 404."""
        create_resp = client.post("/api/categories", json={"name": "Lonely"})
        cat_id = create_resp.json()["id"]

        response = client.put(
            f"/api/categories/{cat_id}",
            json={"parent_id": 9999},
        )
        assert response.status_code == 404


class TestDeleteCategory:
    """Tests for DELETE /api/categories/:id."""

    def test_delete_existing(self, client: TestClient) -> None:
        """Deleting an existing category should return 204."""
        create_resp = client.post("/api/categories", json={"name": "Temp"})
        cat_id = create_resp.json()["id"]

        response = client.delete(f"/api/categories/{cat_id}")
        assert response.status_code == 204

        # Verify it's gone
        get_resp = client.get(f"/api/categories/{create_resp.json()['slug']}")
        assert get_resp.status_code == 404

    def test_delete_nonexistent(self, client: TestClient) -> None:
        """Deleting a nonexistent category should return 404."""
        response = client.delete("/api/categories/9999")
        assert response.status_code == 404

    def test_delete_parent_cascades_children(self, client: TestClient) -> None:
        """Deleting a parent should also delete its children."""
        parent_resp = client.post("/api/categories", json={"name": "Parent"})
        parent_id = parent_resp.json()["id"]

        child_resp = client.post(
            "/api/categories",
            json={"name": "Child", "parent_id": parent_id},
        )
        child_slug = child_resp.json()["slug"]

        # Delete parent
        response = client.delete(f"/api/categories/{parent_id}")
        assert response.status_code == 204

        # Child should also be gone
        get_resp = client.get(f"/api/categories/{child_slug}")
        assert get_resp.status_code == 404


class TestMaxDepth:
    """Tests for maximum category nesting depth enforcement."""

    def test_max_depth_exceeded(self, client: TestClient) -> None:
        """Creating categories beyond max depth should return 400."""
        # Create a chain of depth MAX_CATEGORY_DEPTH
        from routers.categories import MAX_CATEGORY_DEPTH

        current_id = None
        for i in range(MAX_CATEGORY_DEPTH):
            payload: dict = {"name": f"Level {i}"}
            if current_id is not None:
                payload["parent_id"] = current_id
            resp = client.post("/api/categories", json=payload)
            assert resp.status_code == 201, f"Failed at depth {i}: {resp.json()}"
            current_id = resp.json()["id"]

        # This should exceed the max depth
        response = client.post(
            "/api/categories",
            json={"name": "Too Deep", "parent_id": current_id},
        )
        assert response.status_code == 400
        assert "depth" in response.json()["detail"].lower()
