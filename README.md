მოცემული კოდი ემსახურება api-დან მონაცემების წამოღებას და json ფაილში შენახვას სრედების მეშვეობით.

მეთოდი fetch_date არის მეთოდი რომელიც აგზავნის რექვესტებს სერვერზე და წამოთებულ ინფორმაციას json-ის სახით ინახავს ლისტში.

with_treads და with_process ფუნქცია კი 20 სრედს და 5 პროცესს ქმნის რომლებიც პარალელურად მუშაობენ

თითოეული პროცესისთვის 20 სრედი ეშვება, თუმცა ამ რიცხვების შეცვლა რათქმაუნდა შესაძლებელია.

შემდეგ კი შეგროვებულ მონაცემენს ვინახავ json ფაილში to_file მეთოდის გამოყემებით.