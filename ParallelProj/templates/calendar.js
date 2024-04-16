let date = new Date();
let fullYear = date.getFullYear();

function renderCalendar() {
  date.setDate(1);

  const monthDays = document.getElementById("dates");
  const month = document.getElementById("month");
  const daysElement = document.getElementById("days");

  const lastDay = new Date(fullYear, date.getMonth() + 1, 0).getDate();
  const prevLastDay = new Date(fullYear, date.getMonth(), 0).getDate();
  const firstDayIndex = date.getDay();

  const lastDayIndex = new Date(fullYear, date.getMonth() + 1, 0).getDay();

  const nextDays = 6 - lastDayIndex;

  /* i created the list of months like this reduce lines on my end*/
  let months =
    "January February March April May June July August September October November December";
  months = months.split(" ");

  const days = ["S", "M", "T", "W", "T", "F", "S"];

  month.innerText = `${months[date.getMonth()]} ${date.getFullYear()}`;
  daysElement.innerHTML = days.map((day) => `<div>${day}</div>`).join("");

  let dates = "";

  for (let i = firstDayIndex; i > 0; i--)
    dates += `<div class='prev-date'>${prevLastDay - i + 1}</div>`;

  for (let i = 1; i <= lastDay; i++) {
    if (i == new Date().getDate() && date.getMonth() == new Date().getMonth())
      dates += `<div class='today'>${i}</div>`;
    else dates += `<div>${i}</div>`;
  }

  for (let i = 1; i <= nextDays; i++)
    dates += `<div class='next-date'>${i}</div>`;

  monthDays.innerHTML = dates;
}
/* events  */
document.getElementById("prev").addEventListener("click", () => {
  date.setMonth(date.getMonth() - 1);
  renderCalendar();
});

document.getElementById("next").addEventListener("click", () => {
  date.setMonth(date.getMonth() + 1);
  renderCalendar();
});

renderCalendar();
