def validate_inputs(app):
    try:
        name = app.nameInput.text().strip() if hasattr(app, 'nameInput') else ""
        flavor = app.tasteCombo.currentText() if hasattr(app, 'tasteCombo') else ""
        meal_time = get_selected_meal_time(app)
        goal = get_selected_goal(app)
        prep_time = app.prepTimeCombo.currentText() if hasattr(app, 'prepTimeCombo') else ""
        if not name:
            return False, "Nama harus diisi!"
        if not flavor:
            return False, "Pilih rasa makanan!"
        if not meal_time:
            return False, "Pilih waktu makan!"
        if not goal:
            return False, "Pilih tujuan konsumsi!"
        if not prep_time:
            return False, "Pilih waktu persiapan!"
        return True, ""
    except Exception as e:
        return False, "Gagal memvalidasi input!"

def get_selected_meal_time(app):
    try:
        if hasattr(app, 'meal_group'):
            meal_id = app.meal_group.checkedId()
            return {1: "Sarapan", 2: "Makan Siang", 3: "Makan Malam", 4: "Snack"}.get(meal_id)
        return None
    except Exception as e:
        return None

def get_selected_goal(app):
    try:
        if hasattr(app, 'goal_group'):
            goal_id = app.goal_group.checkedId()
            return {1: "Hemat", 2: "Fancy", 3: "Sehat"}.get(goal_id)
        return None
    except Exception as e:
        return None