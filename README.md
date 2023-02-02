<h1 align="center">To-Do List Tool</h1>

<p align="center">
This is a to-do list website. </a></p>



## Links

- [Repo](https://github.com/kelseychristensen/To-Do-List-Website "to-do-tool")

## Screenshots

#### Full-Screen Width
![Full-Screen](/readme-images/full-screen.PNG "Full-Screen")
#### Small Screen
![Small-Screen](/readme-images/small screen.PNG "Sm-Screen")
#### Add an Item Form
![Add Item](/readme-images/add-item.PNG "Add")
#### Edit Item Form
![Edit](/readme-images/edit-item.PNG "Edit")
#### While logged out
![Logged Out](/readme-images/logged-out.PNG "Logged Out")

### Built with

- HTML
- CSS
- Python
- Flask
- Bootstrap
- WTForms 
- Jinja
- SQL

### What went into this project

I created an SQL Database and a Flask Server to serve up the to-do list items tied to a specific user. A user can add, edit, and complete their to-do list items. 

### Continued development

I would love to work with the Due Date piece so that when the date has past, the text is red. And also having it be a date field in the form.
I had a lot of trouble dealing with the datatypes as they get passed around the server. 

```python
@app.route("/complete/<int:item_id>")
def complete(item_id):
    item_to_complete = Item.query.get(item_id)
    item_to_complete.status = 1
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/undo_complete/<int:item_id>")
def undo_complete(item_id):
    item_to_complete = Item.query.get(item_id)
    item_to_complete.status = 0
    db.session.commit()
    return redirect(url_for("home"))
```
```html
    </div>
    <!--     INCOMPLETE ITEM-->
         {% if item.status == 0 %}

            <h1>{{item.title}}</h1>
            <p>{{item.description}}</p>
    <h2>Due: {{item.due_date}}</h2>
                    {% else %}
    <!--     COMPLETED ITEM-->
            <div class="completed-item">
                <h1>{{item.title}}</h1>
                <p>All done!</p>
            </div>
                    {% endif %}
         {% if item.status == 0 %}
         <a class="fa-regular fa-square" href="{{url_for ('complete', item_id=item.id) }}"></i></a>
         {% else %}
         <a class="fa-regular fa-square-check" href="{{url_for ('undo_complete', item_id=item.id) }}"></a></a>
        {% endif %}
    </div>

```
```css
/*FOOTER STYLE*/

footer i {
    padding: 5px;
    color: black;
}

footer i:hover, footer a {
    color: #0f6674;
}

footer a:hover {
    color: grey;
}
```
## Author

Kelsey Christensen

- [Profile](https://github.com/kelseychristensen "Kelsey Christensen")
- [Email](mailto:kelsey.c.christensen@gmail.com?subject=Hi "Hi!")
- [Dribble](https://dribbble.com/kelseychristensen "Hi!")
- [Website](http://kelseychristensen.com/ "Welcome")
