from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)

    # grabs list of project title & name for this student by github
    projects = hackbright.get_grades_by_github(github)

    html = render_template('student_info.html',
                            first=first,
                            last=last,
                            github=github,
                            projects=projects)
    return html


@app.route("/student-add")
def student_add():
    """Add a student."""
    return render_template('student_add.html')


 
@app.route("/student-confirm", methods=["POST"])
def student_confirm():
    
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    if not (first_name or last_name):
        return redirect('/student_add')
    else:
        hackbright.make_new_student(first_name, last_name, github)
        return render_template('student_confirm.html',
                        github=github)


@app.route("/project")
def get_project():
    """Show information about a student."""

    title_request = request.args.get('title') 
    title, description, max_grade = hackbright.get_project_by_title(title_request)

    # get name, grade by guthub......
    # github, grade
    githubs_and_grades = hackbright.get_grades_by_title(title)

    student_grades = []

    for github, grade in githubs_and_grades:
        # github_and_grade = [github_and_grade]
        student = hackbright.get_student_by_github(github)
        name = student[0:2]
        github_grade_names = (github, grade) + name
        student_grades.append(github_grade_names)


        # github_and_grade.append(name)
    

    html = render_template('project_info.html',
                            title=title,
                            description=description,
                            max_grade=max_grade,
                            student_grades=student_grades)
    return html

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
