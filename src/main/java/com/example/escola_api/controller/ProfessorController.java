package com.example.escola_api.controller;

import com.example.escola_api.model.entity.Professor;
import com.example.escola_api.model.service.ProfessorService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.List;

@RestController
@RequestMapping("/professores")
public class ProfessorController {

    private final ProfessorService professorService;

    public ProfessorController(ProfessorService professorService) {
        this.professorService = professorService;
    }

    @PostMapping
    public ResponseEntity<Professor> criarProfessor(@Valid @RequestBody Professor professor) {
        Professor salvo = professorService.criarProfessor(professor);
        return ResponseEntity
                .created(URI.create("/professores/" + salvo.getId()))
                .body(salvo);
    }

    @GetMapping
    public ResponseEntity<List<Professor>> listarProfessores() {
        return ResponseEntity.ok(professorService.listarProfessores());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Professor> buscarPorId(@PathVariable Long id) {
        return professorService.buscarPorId(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PutMapping("/{id}")
    public ResponseEntity<Professor> atualizarProfessor(@PathVariable Long id,
                                                        @Valid @RequestBody Professor professor) {
        Professor atualizado = professorService.atualizarProfessor(id, professor);
        return ResponseEntity.ok(atualizado);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletarProfessor(@PathVariable Long id) {
        professorService.deletarProfessor(id);
        return ResponseEntity.noContent().build();
    }
}
