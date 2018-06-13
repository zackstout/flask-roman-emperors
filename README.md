# Flask Roman Emperors
Working with this [dataset](https://github.com/zonination/emperors/blob/master/emperors.csv) to uncover patterns and learn more about Pandas.

## Flask:
Ok, flask seems pretty easy. We can:
- Route to different pages; can presumably be hit by AJAX requests;
- Pass data into our HTML templates;
- Return images of matplotlib charts to the client.

## Pandas:
And we're making progress with the data analysis via Pandas. Ideas:

- [ ] Would be good to write a function that checks how many of those (e.g.) from Italia assassinated, VS how often *everyone* was assassinated;
- [x] Find length of life and length of reign;
- [ ] Find distance of birth city from Rome;
- [ ] Check how they rose against how they died for strong correlations (use linear regression module);
- [ ] Like with Footprint app, let user choose a category (e.g. cause of death), a particular (assassination), and then a slice (province of birth, killer, length of reign -- though this would want to chunked into like 0-5, 5-10 years, etc.);
- [ ] Map chronologically as a kind of diagonal, with reign colored bold and lifespan colored lightly. Different color by dynasty.
- [ ] Avg. length of reign by killer, or by dynasty
- [ ] Chart causes of death as lines against time.
- [ ] I wonder what the best way to handle the BC values is... just manually add "neg" to them in the CSV and then interpret them as negative numbers?
