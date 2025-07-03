import { Component } from '@angular/core';
import {MatCard, MatCardModule} from "@angular/material/card";
import {MatExpansionModule} from "@angular/material/expansion";
import {MatChipsModule} from "@angular/material/chips";
import {MatIconModule} from "@angular/material/icon";

@Component({
  selector: 'app-api-documentation',
  imports: [
    MatCardModule,
      MatExpansionModule,
      MatChipsModule,
MatIconModule,
  ],
  templateUrl: './api-documentation.component.html',
  styleUrl: './api-documentation.component.scss'
})
export class ApiDocumentationComponent {

}
