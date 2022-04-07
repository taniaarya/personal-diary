import click
from datetime import datetime
from diary import Diary


@click.group()
def commands():
    """
    Welcome to your Personal Diary.\f

    Displays the welcome message in this docstring when running the script.
    """
    pass


@click.command(name='view_all')
def view_entries():
    """
    View an overview of your existing diary entries.\f

    Displays a list of existing diary entries in reverse chronological order such that entries with the highest IDs
    are shown first.
    """
    existing_entries = diary.read_from_db()
    if len(existing_entries) == 0:
        click.echo("No entries exist yet.")
        return

    click.echo("Existing entries:\n")
    for entry_id, entry_data in sorted(existing_entries.items(), reverse=True):
        click.echo("Entry ID: " + entry_id)
        click.echo("Date Created: " + entry_data.get("date_created"))
        click.echo("Title: " + entry_data.get("title"))
        click.echo("_______________________________________________")


@click.command(name='create')
def create_entry():
    """
    Create a new diary entry.\f

    Prompts the user to enter a title and body text to create a new diary entry.
    The title and body text entered are passed on to the backend.
    If no text is entered for the body, then a new entry is not created.
    """
    entry_title = click.prompt("\nEnter a title for the diary entry")

    click.echo("\nIn the launched text editor, enter in the body text for the diary entry. "
               "\nBe sure to save before closing the editor.")
    entry_body = click.edit()
    if entry_body is None:
        click.echo("\nNothing was written or the editor was closed without saving. Create operation canceled.")
        return

    diary.create_entry({"title": entry_title,
                        "body": entry_body,
                        "datetime": datetime.now()})
    click.echo("\nYour diary entry has been created.")


@click.command(name='read')
def read_entry():
    """
    Read an existing diary entry.\f

    Prompts the user to enter an id of an existing diary entry to print out to the command line.
    If an invalid ID is entered, then the operation terminates.
    """
    entry_id = click.prompt("\nEnter the ID of an existing diary entry to read", type=int)

    if diary.is_id_invalid(entry_id):
        click.echo("No entry matches that ID. Read operation canceled.")
        return

    selected_entry = diary.read_entry({"entry_id": entry_id})
    click.echo("Title: " + selected_entry.get("title"))
    click.echo("Body: " + selected_entry.get("body"))


@click.command(name='edit')
def update_entry():
    """
    Edit an existing diary entry.\f

    Prompts the user to enter the ID of an existing diary entry, which they can then edit the title or body text of.
    By default, the original entry will just stay the same if no entries are made. If an invalid ID is entered, then
    the operation terminates.
    """
    entry_id = click.prompt("\nEnter the ID of an existing diary entry to edit", type=int)

    if diary.is_id_invalid(entry_id):
        click.echo("No entry matches that ID. Edit operation canceled.")
        return

    original_entry = diary.read_from_db().get(str(entry_id))
    original_title = original_entry.get("title")
    original_body = original_entry.get("body")

    click.echo("Original title: " + original_title)
    edited_title = click.prompt("Enter an updated title", default=original_title, show_default=False)
    click.echo("\nIn the launched text editor, enter in the updated body text for the diary entry."
               "\nBe sure to save before closing the editor or else no changes will be made.")

    edited_body = click.edit(original_body)
    if edited_body is None:
        click.echo("No changes were made or the editor was closed without saving.")
        edited_body = original_body

    diary.create_entry({"title": edited_title,
                        "body": edited_body})
    click.echo("\nAny edits to the entry title or body have been saved.")


@click.command(name='delete')
def delete_entry():
    """Delete an existing diary entry.\f

    Prompts the user to enter the ID of an existing diary entry to delete.
    If an invalid ID is entered, then the operation terminates.
    """
    entry_id = click.prompt("\nEnter the ID of an existing diary entry to delete", type=int)

    if diary.is_id_invalid(entry_id):
        click.echo("No entry matches that ID. Delete operation canceled.")
        return

    if not click.confirm('Are you sure you want to delete this entry?'):
        click.echo("\nDelete operation canceled.")
        return

    diary.delete_entry({"entry_id": entry_id})
    click.echo("\nEntry has been deleted.")


diary = Diary()
commands.add_command(view_entries)
commands.add_command(create_entry)
commands.add_command(read_entry)
commands.add_command(update_entry)
commands.add_command(delete_entry)

if __name__ == '__main__':
    commands()
