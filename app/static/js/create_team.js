'use strict';

const selfIsCoachCheckbox = document.querySelector('#user_is_coach');
const coachDropdown = document.querySelector('#coach_dropdown');

selfIsCoachCheckbox.addEventListener('change', (event) => {
    if (event.currentTarget.checked)
        coachDropdown.classList.add('hidden');
    else
        coachDropdown.classList.remove('hidden');
})