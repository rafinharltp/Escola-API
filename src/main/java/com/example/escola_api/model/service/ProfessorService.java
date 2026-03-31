package com.example.escola_api.model.service;

import com.example.escola_api.model.entity.Professor;
import com.example.escola_api.model.repository.ProfessorRepository;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.Optional;

@Service
public class ProfessorService {

    private final ProfessorRepository professorRepository;

    public ProfessorService(ProfessorRepository professorRepository) {
        this.professorRepository = professorRepository;
    }

    public Professor criarProfessor(Professor professor) {
        return professorRepository.save(professor);
    }

    public List<Professor> listarProfessores() {
        return professorRepository.findAll();
    }

    public Optional<Professor> buscarPorId(Long id) {
        return professorRepository.findById(id);
    }

    public Professor atualizarProfessor(Long id, Professor dadosAtualizados) {
        return professorRepository.findById(id)
                .map(professor -> {
                    professor.setNome(dadosAtualizados.getNome());
                    professor.setEspecialidade(dadosAtualizados.getEspecialidade());
                    return professorRepository.save(professor);
                })
                .orElseThrow(() -> new ResponseStatusException(
                        HttpStatus.NOT_FOUND, "Professor não encontrado"));
    }

    public void deletarProfessor(Long id) {
        if (!professorRepository.existsById(id)) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Professor não encontrado");
        }
        professorRepository.deleteById(id);
    }
}
