<div class="flex items-center">
          <input
              type="checkbox"
              id="stat"
              name="stat"
              class="mr-2"
              value="1"
              {% if materiel.stat == True or materiel.stat == '1' %}checked{% endif %}
            />

          <label for="stat" class="text-gray-700 font-semibold"
            >Disponible</label
          >
        </div>
        <div class="flex items-center">
          <input
            type="checkbox"
            id="repere"
            name="repere"
            class="mr-2"
            value="1"
            {%
            if
            materiel.repere == True or materiel.repere == '1'
            %}checked{%
            endif
            %}
          />
          <label for="repere" class="text-gray-700 font-semibold">Repéré</label>
        </div>



<div class="flex items-center">
          <input
            type="checkbox"
            id="stat"
            name="stat"
            class="mr-2"
            value="1"
            {%
            if
            materiel.stat==True or materiel.stat=='1'
            %}checked{%
            endif
            %}
          />
          <label for="stat" class="text-gray-700 font-semibold"
            >Disponible</label
          >
        </div>
        <div class="flex items-center">
          <input
            type="checkbox"
            id="repere"
            name="repere"
            class="mr-2"
            value="1"
            {%
            if
            materiel.repere==True or materiel.repere=='1'
            %}checked{%
            endif
            %}
          />
          <label for="repere" class="text-gray-700 font-semibold">Repéré</label>
        </div>